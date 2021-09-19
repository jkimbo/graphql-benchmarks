import json
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

colors = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
]


def get_data(results, fn):
    all_servers = [result["server_name"] for result in results]
    query_results = [result["results"] for result in results]

    return [
        {
            "x": all_servers,
            "y": list(map(fn, query_results)),
            "type": "bar",
            "name": all_servers,
            "marker": {
                "color": colors,
            },
        }
    ]


def get_ymetric_fn(yMetric, on="latency"):
    if yMetric == "P95":

        def yMetricFn(x):
            return x[on]["dist"]["95"]

    elif yMetric == "P98":

        def yMetricFn(x):
            return x[on]["dist"]["98"]

    elif yMetric == "P99":

        def yMetricFn(x):
            return x[on]["dist"]["99"]

    elif yMetric == "MIN":

        def yMetricFn(x):
            return x[on]["min"]

    elif yMetric == "MAX":

        def yMetricFn(x):
            return x[on]["max"]

    else:

        def yMetricFn(x):
            return x[on]["mean"]

    if on == "latency":
        return lambda x: round(yMetricFn(x) / 1000, 2)

    return lambda x: int(yMetricFn(x))


with open("./results.json", "r") as json_file:
    bench_results = json.load(json_file)


app = dash.Dash()

app.layout = html.Div(
    children=[
        html.Label("Response time metric"),
        dcc.Dropdown(
            id="response-time-metric",
            options=[
                {"label": "P95", "value": "P95"},
                {"label": "P98", "value": "P98"},
                {"label": "P99", "value": "P99"},
                {"label": "Min", "value": "MIN"},
                {"label": "Max", "value": "MAX"},
                {"label": "Average", "value": "AVG"},
            ],
            value="AVG",
        ),
        dcc.Graph(id="response-time-vs-query"),
        dcc.Graph(id="requests-vs-query"),
    ]
)


@app.callback(
    Output("response-time-vs-query", "figure"),
    [
        # Input('benchmark-index', 'value'),
        Input("response-time-metric", "value")
    ],
)
def update_graph(yMetric):
    figure = {
        "data": get_data(bench_results["results"], get_ymetric_fn(yMetric, on="latency")),
        "layout": {
            "yaxis": {"title": "Response time ({}) in ms".format(yMetric)},
            "xaxis": {"title": "API", "categoryorder": "total descending"},
            "title": "Response time by API",
        },
    }
    return figure


@app.callback(
    Output("requests-vs-query", "figure"),
    [
        # Input('benchmark-index', 'value'),
        Input("response-time-metric", "value")
    ],
)
def update_graph2(yMetric):
    figure = {
        "data": get_data(bench_results["results"], get_ymetric_fn(yMetric, on="requests")),
        "layout": {
            "yaxis": {"title": "Requests/s ({})".format(yMetric)},
            "xaxis": {"title": "API", "categoryorder": "total descending"},
            "title": "Reqs/s by API",
        },
    }
    return figure


app.run_server(host="0.0.0.0", port=8080, debug=True)
