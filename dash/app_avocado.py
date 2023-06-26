import pandas as pd
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go


data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)


regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()

app = Dash(__name__)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Avocado Analytics"
                ),
                html.P(
                    children=(
                        "Analyze the behavior of avocado prices and the number"
                        " of avocados sold in the US between 2015 and 2018"
                    ),
                ),
            ],
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value="Albany",
                            clearable=False,
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": avocado_type.title(),
                                    "value": avocado_type,
                                }
                                for avocado_type in avocado_types
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    price_chart_figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_data["Date"],
                y=filtered_data["AveragePrice"],
                mode="lines",
                hovertemplate="$%{y:.2f}<extra></extra>",
            ),
        ],
        layout=go.Layout(
            title={
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            xaxis={"fixedrange": True},
            yaxis={"tickprefix": "$", "fixedrange": True},
            colorway=["#17B897"],
        ),
    )

    volume_chart_figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_data["Date"],
                y=filtered_data["Total Volume"],
                mode="lines",
            ),
        ],
        layout=go.Layout(
            title={"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            xaxis={"fixedrange": True},
            yaxis={"fixedrange": True},
            colorway=["#E12D39"],
        ),
    )
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)