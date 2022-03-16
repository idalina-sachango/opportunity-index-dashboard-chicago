import plotly.graph_objects as go
import pandas as pd
import json
import geopandas as gpd
import numpy as np
from pandas.io.json import json_normalize
from pathlib import Path


def make_fig():
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

    #cps_locations = open_path("cps-geojson.geojson", "school_id")
    census_tract = open_path("census_tract.geojson", "geoid10")

    df2 = pd.read_csv(data_path_results.joinpath("indicators_by_school_unscaled.csv"), dtype={"School ID": str})
    df2 = pd.DataFrame(df2)
    df2['pov_rate'] = 100 - df2['above_pov_rate']

    acs = pd.read_csv(data_path_acs.joinpath("acs_data_1.csv"))
    acs = pd.DataFrame(acs)

    print(df2['pov_rate'])


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
    

    #plot bubbles with cps college data
    fig.add_trace(go.Scattergeo(
        lon = df2['longitude'],
        lat = df2['latitude'],
        text = df2["school_name"],
        marker_color='white',
        marker_size=df2['college_enroll_pct'] * 15,
        showlegend=True,
        visible=False))
        
    

    fig.update_traces(customdata=df2[['college_enroll_pct', 'pov_rate', 'census_tract']])
    fig.update_traces(hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' + 
                                    '<b>% Poverty Rate:</b> %{customdata[1]}<br>' +
                                    '<b>% College Enrollment:</b> %{customdata[0]}<br>' +
                                    '<b>% Census Tract:</b> %{customdata[2]}<br>')

    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=census_df["geoid10"],
        z = acs['pov_rate_cleaned'],
        showscale=True,
        hoverinfo='skip',
        visible=False
    ))

    fig.update_geos(fitbounds="locations", visible=True)
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')

    fig.update_layout(
        title_text = 'Poverty Rate',
        geo_scope='usa', # limite map scope to USA,
    )

    fig.update_coloraxes(showscale=False)

    return fig


