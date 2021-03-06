import plotly.graph_objects as go
import pandas as pd
import json
import geopandas as gpd
import numpy as np
from pathlib import Path


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
    data_path_results = home_path.joinpath("data/results")
    data_path_acs = home_path.joinpath("data/acs")
    data_path_geo = home_path.joinpath("data/geojson")


    def open_path(filename, feature):
        with open(data_path_geo.joinpath(filename)) as f:
            df = json.load(f)
        for i in range(len(df["features"])):
            df["features"][i]["id"] = df["features"][i]["properties"][feature]
        return df

    census_df = gpd.read_file(data_path_geo.joinpath("census_tract.geojson"))
    census_df["blank_bounds"] = 0
    census_df = census_df[["geoid10", "blank_bounds"]]

    census_tract = open_path("census_tract.geojson", "geoid10")

    df = pd.read_csv(data_path_results.joinpath("indicators_by_school_unscaled.csv"), dtype={"School ID": str})
    df = pd.DataFrame(df)
    df['pov_rate'] = round(100 - df['above_pov_rate'], 2)

    acs = pd.read_csv(data_path_acs.joinpath("acs_data_1.csv"))
    acs = pd.DataFrame(acs)


    acs['pov_rate_cleaned'] = np.select(
        [
            acs['pov_rate'].between(-666666666.0, 0, inclusive=True)
        ], 
        [
            0
        ], 
        default=acs['pov_rate']
    )


    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df["school_name"],
        marker_color='white',
        marker_size=df['college_enroll_pct'] * 0.2,
        showlegend=False,
        visible=False))
        

    fig.update_traces(customdata=df[['college_enroll_pct', 'pov_rate', 'census_tract']])
    fig.update_traces(hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' + 
                                    '<b>Poverty Rate:</b> %{customdata[1]}<br>' +
                                    '<b>College Enrollment:</b> %{customdata[0]}<br>' +
                                    '<b>Census Tract:</b> %{customdata[2]}<br>')

    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=census_df["geoid10"],
        z = acs['pov_rate_cleaned'],
        showscale=True,
        hoverinfo='skip',
        visible=False,
        colorbar_title='Poverty Rate'
    ))

    fig.update_geos(fitbounds="locations", visible=True)

    fig.update_layout(
        geo_scope='usa'
    )

    fig.update_coloraxes(showscale=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')
    return fig


