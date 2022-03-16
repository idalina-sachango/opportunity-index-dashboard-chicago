from asyncio import run
import plotly.graph_objects as go
import pandas as pd
import json
import geopandas as gpd
from pandas.io.json import json_normalize
from pathlib import Path
import scatter, air_pollution, college, poverty_rate


def run_all():
    home_path = Path(__file__).parent.parent
    data_path = home_path.joinpath("data/results")
    data_path_geo = home_path.joinpath("data/geojson")

    scatter_fig = scatter.make_fig()
    college_fig = college.make_fig()
    poverty_fig = poverty_rate.make_fig()

    fig = go.Figure()

    fig.update_geos(fitbounds="locations", visible=True)
    fig.add_traces(scatter_fig.data)
    fig.add_traces(college_fig.data)
    fig.add_traces(poverty_fig.data)


    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Opportunity Index by School",
                         method="update",
                         args=[{"visible": [False,True,True,True,True,True,False,False,False]},
                               {"title": "Opportunity index mapping"}]),
                    dict(label="College Enrollment Percentage by School",
                         method="update",
                         args=[{"visible": [False, False,False,False,False,False,True,True,False]},
                               {"title": "College enrollment index mapping"}]),
                    dict(label="Poverty Rate x College Enrollment",
                         method="update",
                         args=[{"visible": [False,False,False,False,False,False,False,False,True,True]},
                               {"title": "College enrollment index mapping to poverty rate"}])
                ]),
                type = "buttons",
                direction="left",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="left",
                yanchor="top"

            )

        ]

    )
    fig.show()
    return None

run_all()