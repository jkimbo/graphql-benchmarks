import json
import docker
import os
import asyncio
import yaml
from functools import reduce

import numpy as np

client = docker.from_env()

def load_config():
    with open('config.yaml', 'r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return config


async def run_single_benchmark(tag, query):
    query_slug = query['name'].replace(" ", "-")
    output_file = f"results/{tag}-{query_slug}-results.json"

    benchmark_process = await asyncio.create_subprocess_shell(
        f"k6 run --out json={output_file} {query['runner']}",
    )
    await benchmark_process.wait()

    data_points = []

    # convert data to proper json format
    with open(output_file, "r") as results_file:
        while True:
            line = results_file.readline()

            if not line:
                break # EOF

            result = json.loads(line)
            if result['type'] == "Point":
                data_points.append(result)

    return data_points 

async def run_all_benchmarks():
    config = load_config()
    results = []

    for server in config["servers"]:
        server_name = server['name']
        server_path = server['path']
        server_tag = server_path.strip('/').split('/')[-1]

        if not os.path.isfile(f"{server_path}/Dockerfile"):
            print(f'Skipping {server_name}.')
            continue

        print(f"Building image for {server_name}...")
        client.images.build(path=f"{server_path}", tag=server_tag)
        print(f"Finished building image for {server_name}.\n")

        print(f"Starting {server_name} server...")
        container = client.containers.run(
            server_tag,
            detach=True,
            mem_limit='1g',
            ports={'8000/tcp': 8000}
        )
        print(f"{server_name} server running.\n")
        try:
            # Wait for server to boot
            await asyncio.sleep(2)

            for query in config['queries']:
                if 'runner' not in query:
                    continue

                print(f"Running {query['name']} benchmarks for {server_name}...")
                data_points = await run_single_benchmark(server_tag, query)
                print(f"Completed {query['name']} benchmarks for {server_name}.")

                
                request_duration_results = filter(
                    lambda r: r['metric'] == 'http_req_duration',
                    data_points
                )
                request_durations = list(map(lambda r: r['data']['value'],  request_duration_results))
                requests = len(list(filter(
                    lambda r: r['metric'] == 'http_reqs',
                    data_points
                )))

                results.append({
                    "query_name": query['name'],
                    "server_name": server_name,
                    "results": {
                        "latency": {
                            "max": np.max(request_durations) * 1000,
                            "min": np.min(request_durations) * 1000,
                            "mean": np.mean(request_durations) * 1000,
                            "dist": {
                                "95": np.percentile(request_durations, 95) * 1000,
                                "98": np.percentile(request_durations, 98) * 1000,
                                "99": np.percentile(request_durations, 99) * 1000,
                            },
                            "stdev": np.std(request_durations) * 1000
                        },
                        "requests": {
                            "max": requests / 15,
                            "min": requests / 15,
                            "mean": requests / 15,
                            "dist": {
                                "95": requests / 15,
                                "98": requests / 15,
                                "99": requests / 15,
                            },
                            "stdev": requests / 15
                        },
                    }
                })

            print(f"Killing {server_name} server...")
            container.kill()
            print(f"{server_name} server killed. \n")
        except Exception:
            container.kill()
            raise
    
    with open('./results.json', 'w') as results_file:
        json.dump(results, results_file)


if __name__ == '__main__':
    asyncio.run(run_all_benchmarks())