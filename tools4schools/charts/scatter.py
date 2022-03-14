
import plotly.graph_objects as go
import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path


def make_fig():
    home_path = Path(__file__).parent.parent
    data_path = home_path.joinpath("Project/Output")
    data_test = home_path.joinpath("data")
    data_path_geo = home_path.joinpath("data/geojson")


    def open_path(filename, feature):
        with open(data_path_geo.joinpath(filename)) as f:
            df = json.load(f)
        for i in range(len(df["features"])):
            df["features"][i]["id"] = df["features"][i]["properties"][feature]
        return df

    #cps_locations = open_path("cps-geojson.geojson", "school_id")
    census_tract = open_path("census_tract.geojson", "geoid10")

    df2 = pd.read_csv(data_path.joinpath("opportunity_index_by_school_scaled.csv"), dtype={"School ID": str})
    df2 = pd.DataFrame(df2)
    df2 = df2.assign(opportunity_ranked = pd.qcut(df2.opportunity_index, 5, labels = [1, 2, 3, 4, 5]))

    #merge cps college data with csv with latitude longitude for schools
    #full = pd.merge(df2, df, on='schoolid',  how='left')

    df3 = pd.read_csv(data_test.joinpath("chi_air.csv"), dtype={"ctfips": str})
    df3 = df3.fillna(999)
    df3 = pd.DataFrame(df3)
    df3["blank_bounds"] = 0

    #colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    fig = go.Figure()

    #plot bubbles with cps college data
    for _, row in df2.iterrows():
        fig.add_trace(go.Scattergeo(
        lon = [row['longitude']],
        lat = [row['latitude']],
        showlegend=False,
        marker_color=[row['opportunity_ranked']],
        marker_cmin=1,
        marker_cmax=5,
        marker_colorscale='ylorrd'))

    # draw census tract boundariess
    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=df3["ctfips"],
        z = df3["blank_bounds"],
        showscale=False
    ))

    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_layout(
        title_text = 'College Enrollment by School',
        geo_scope='usa', # limite map scope to USA,
        showlegend=False
    )
    fig.update_coloraxes(showscale=False)

    return fig