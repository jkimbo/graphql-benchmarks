# GraphQL benchmarks

GBench is a GraphQL benchmarking tool. It's highly inspired by Hasura's work on [graphql-bench](https://github.com/hasura/graphql-bench/) but with different design and goals in mind.

Gbench will use a [config file](#config-file) to read the servers and queries to be executed.

## Requirements

If you want to run gbench locally, you will need Python 3.7+, poetry, docker and `k6` working locally.

```shell
poetry install
# For mac
brew install k6
```

## Run benchmarks

```bash
poetry run python gbench.py
```

## View dashboard

```bash
poetry run python dashboard.py
```

## Config file

The Gbench config file is in a `yaml` format. It have two main sections: `servers` and `queries`.

The `servers` section indicates in which servers we are going to run the benchmark.
Each server is built as a docker container that exposes a GraphQL endpoint on port 8000.

```yaml
servers:
- name: Django + Graphene v3
  path: servers/django-graphene/
```

The `queries` section indicates all the different queries that we want to benchmark, in all servers.

```yaml
queries:
- name: Top 250 rated movies
  # K6 benchmark file
  runner: queries/top-movies.js
```
