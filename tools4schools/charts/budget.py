import pandas as pd
import geopandas as gpd
from pathlib import Path 
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np


def make_fig():
    home_path = Path(__file__).parent.parent 
    data_path = home_path.joinpath("data/results")
    data_path_geo = home_path.joinpath("data/geojson")


    def open_path(filename, feature):
        with open(data_path_geo.joinpath(filename)) as f:
            df = json.load(f)
        for i in range(len(df["features"])):
            df["features"][i]["id"] = df["features"][i]["properties"][feature]
        return df


    census_tract = open_path("census_tract.geojson", "geoid10")
    census_df = gpd.read_file(data_path_geo.joinpath("census_tract.geojson"))
    census_df["blank_bounds"] = 0
    census_df = census_df[["geoid10", "blank_bounds"]]

    fig = go.Figure()
    df = pd.read_csv(data_path.joinpath("indicators_by_school_per_unit.csv"), dtype={"census_tract": str})
    df = df.fillna(999)
    df = pd.DataFrame(df)
    df["blank_bounds"] = 0
    df.rename(columns={"FY 2017 Ending Budget": "budget_per_student"}, inplace=True)


    #create base census tract map
    fig.add_trace(go.Choropleth(geojson=census_tract,featureidkey="properties.geoid10",
        locations=census_df["geoid10"],
        z = census_df["blank_bounds"],
        showscale=False,
    ))

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        hovermode='x')


    #create bubbles
    colors = {"Small School": "#8F00FF", "Medium School": "#6495ED", "Large School": "#FFBF00"}
    df['grouping'] = np.select(
        [
            df["enrollment_crdc"].between(0, 200, inclusive=False), 
            df["enrollment_crdc"].between(200, 1000, inclusive=False),
            df["enrollment_crdc"].between(1000, 5000, inclusive=False),
        ], 
        [
            'Small School', 
            'Medium School',
            'Large School'
        ], 
        default='Unknown'
    )


    for _,label in enumerate(df["grouping"].unique()):
        fig.add_trace(go.Scattergeo(
        lat = df["latitude"][df["grouping"] == label],
        lon = df["longitude"][df["grouping"] == label],
        showlegend = True,
        marker = dict(size = (df["budget_per_student"][df["grouping"] == label]) * 0.02,
        color = colors[label], 
        opacity = 0.5,
        line_color='rgb(40,40,40)', 
        line_width=0.5,
        sizemode = 'area'),
        name = label,
        text = pd.Series(df["school_name"][df["grouping"] == label]),
        customdata= pd.Series(round(df["budget_per_student"][df["grouping"] == label], 2)),
        hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' + 
                                        '<b>Budget per Student:</b> %{customdata}',
        hoverinfo = "text"
        ))

    fig.update_coloraxes(showscale=False)
    fig.update_layout(legend_title = "School Size")
    return fig