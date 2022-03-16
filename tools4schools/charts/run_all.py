from asyncio import run
import plotly.graph_objects as go
import pandas as pd
import json
import geopandas as gpd
from pandas.io.json import json_normalize
from pathlib import Path
from tools4schools.charts import scatter, college, poverty_rate, budget


def run_all():

    scatter_fig = scatter.make_fig()
    college_fig = college.make_fig()
    poverty_fig = poverty_rate.make_fig()
    budget_fig = budget.make_fig()

    fig = go.Figure()

    fig.update_geos(fitbounds="locations", visible=True)
    fig.add_traces(scatter_fig.data)
    fig.add_traces(college_fig.data)
    fig.add_traces(poverty_fig.data)
    fig.add_traces(budget_fig.data)


    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Opportunity Index by School",
                         method="update",
                         args=[{"visible": [True,True,True,
                                            True,True,True,
                                            False,False,False,
                                            False,False,False,
                                            False,False]},
                               {"title": "Opportunity index mapping"}]),
                    dict(label="College Enrollment Percentage by School",
                         method="update",
                         args=[{"visible": [False,False,False,
                                            False,False,False,
                                            True,True,False,
                                            False,False,False,
                                            False,False]},
                               {"title": "College enrollment index mapping"}]),
                    dict(label="Poverty Rate x College Enrollment",
                         method="update",
                         args=[{"visible": [False,False,False,
                                            False,False,False,
                                            False,False,True,
                                            True,False,False,
                                            False,False]},
                               {"title": "College enrollment index mapping to poverty rate"}]),
                    dict(label="Budget by school",
                         method="update",
                         args=[{"visible": [False,False,False,
                                            False,False,False,
                                            False,False,False,
                                            False,True,True,
                                            True,True]},
                               {"title": "Budget by school"}])
                ]),
                type = "buttons",
                direction="left",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.2,
                xanchor="left",
                yanchor="top"

            )

        ]

    )
    return fig