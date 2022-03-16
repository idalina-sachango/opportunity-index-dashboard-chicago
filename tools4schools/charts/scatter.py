import json
from pathlib import Path
import geopandas as gpd
import numpy as np
import plotly.graph_objects as go
import pandas as pd


def make_fig():
    """
    Create the plotly figure that corresponds to
    the indicator of interest. Sets the path to files, 
    opens geojson's, and does any figure specific 
    transformations.
    Inputs: None
    Outputs: Plotly figure
    """
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

    census_tract = open_path("census_tract.geojson", "geoid10")

    df = pd.read_csv(data_path.joinpath("opportunity_index_by_school_scaled.csv"),
                      dtype={"School ID": str})
    df = pd.DataFrame(df)


    df['opportunity_ranked'] = np.select(
        [
            df['opportunity_index'].between(0, 20, inclusive=True),
            df['opportunity_index'].between(20, 40, inclusive='right'),
            df['opportunity_index'].between(40, 60, inclusive='right'),
            df['opportunity_index'].between(60, 80, inclusive='right'),
            df['opportunity_index'].between(80, 100, inclusive='right')
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


    pd.to_numeric(df['opportunity_ranked'])
    fig = go.Figure()

    for _, row in enumerate(df['opportunity_ranked'].unique()):
        fig.add_trace(go.Scattergeo(
        lon = df['longitude'][df['opportunity_ranked'] == row],
        lat = df['latitude'][df['opportunity_ranked'] == row],
        text = df['school_name'][df['opportunity_ranked'] == row],
        marker_color=df['opportunity_ranked'][df['opportunity_ranked'] == row].astype(int),
        marker_cmin=1,
        marker_cmax=5,
        marker_colorscale='rdylgn',
        marker_size=10,
        legendgrouptitle=dict(text='Opportunity Ranking'),
        showlegend=True,
        name=row,
        customdata=df["opportunity_index"][df['opportunity_ranked'] == row],
        hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' +
                                        '<b>Opportunity Index:</b> %{customdata}'
        ))


    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=census_df["geoid10"],
        z = census_df["blank_bounds"],
        showscale=False,
        hoverinfo='skip',
        legendgrouptitle=dict(text = 'Opportunity Index Rankings')
    ))

    fig.update_geos(fitbounds="locations", visible=True)

    fig.update_layout(
        geo_scope='usa'
    )

    fig.update_coloraxes(showscale=False)
    fig.update_layout(legend_title = "Opportunity Index Rankings")

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    return fig
