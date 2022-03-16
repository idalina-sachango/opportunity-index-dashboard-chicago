
import plotly.graph_objects as go
import pandas as pd
import json
import geopandas as gpd
import numpy as np
from pandas.io.json import json_normalize
from pathlib import Path


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

    #make census df from geojson
    census_tract = open_path("census_tract.geojson", "geoid10")


    census_df = gpd.read_file(data_path_geo.joinpath("census_tract.geojson"))
    census_df["blank_bounds"] = 0
    census_df = census_df[["geoid10", "blank_bounds"]]

    #cps_locations = open_path("cps-geojson.geojson", "school_id")
    census_tract = open_path("census_tract.geojson", "geoid10")

    df2 = pd.read_csv(data_path.joinpath("opportunity_index_by_school_scaled.csv"), dtype={"School ID": str})
    df2 = pd.DataFrame(df2)
    # df2 = df2.assign(opportunity_ranked = pd.qcut(df2.opportunity_index, 5, labels = [1, 2, 3, 4, 5]))

    df2['opportunity_ranked'] = np.select(
        [
            df2['opportunity_index'].between(0, 20, inclusive=True), 
            df2['opportunity_index'].between(20, 40, inclusive='right'),
            df2['opportunity_index'].between(40, 60, inclusive='right'),
            df2['opportunity_index'].between(60, 80, inclusive='right'),
            df2['opportunity_index'].between(80, 100, inclusive='right')
        ], 
        [
            1, 
            2,
            3,
            4,
            5
        ], 
        default='Unknown'
    )

    pd.to_numeric(df2['opportunity_ranked'])

    fig = go.Figure()


    for _, row in enumerate(df2['opportunity_ranked'].unique()):
        fig.add_trace(go.Scattergeo(
        lon = df2['longitude'][df2['opportunity_ranked'] == row],
        lat = df2['latitude'][df2['opportunity_ranked'] == row],
        text = df2['school_name'][df2['opportunity_ranked'] == row],
        marker_color=df2['opportunity_ranked'][df2['opportunity_ranked'] == row].astype(int),
        marker_cmin=1,
        marker_cmax=5,
        marker_colorscale='rdylgn',
        showlegend=True,
        name=row,
        customdata=df2["opportunity_index"][df2['opportunity_ranked'] == row],
        hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' + 
                                        '<b>Opportunity Index:</b> %{customdata}'
        
        
        ))


    # draw census tract boundariess
    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=census_df["geoid10"],
        z = census_df["blank_bounds"],
        showscale=False,
        hoverinfo='skip'
    ))

    fig.update_geos(fitbounds="locations", visible=True)
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    fig.update_layout(
        title_text = 'College Enrollment by School',
        geo_scope='usa'
    )

    fig.update_coloraxes(showscale=False)

    return fig