from asyncio import run
import plotly.graph_objects as go
import pandas as pd
import json
import geopandas as gpd
from pandas.io.json import json_normalize
from pathlib import Path
from tools4schools.charts import scatter, air_pollution


def run_all():
    home_path = Path(__file__).parent.parent
    data_path = home_path.joinpath("data/results")
    data_path_geo = home_path.joinpath("data/geojson")

    scatter_fig = scatter.make_fig()
    air_fig = air_pollution.make_fig()
    fig = go.Figure()

    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_traces(scatter_fig.data)
    fig.add_traces(air_fig.data)


    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Opportunity Index",
                         method="update",
                         args=[{"visible": [True, True, False]},
                               {"title": "Opportunity index mapping"}]),
                    dict(label="Air Pollution",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Air pollution index mapping"}])
                ]),
                type = "buttons",
                direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="left",
                yanchor="top"

            )

        ]

    )

    return fig