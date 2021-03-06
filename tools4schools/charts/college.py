import json
from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd



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

    census_df = gpd.read_file(data_path_geo.joinpath("census_tract.geojson"))
    census_df["blank_bounds"] = 0
    census_df = census_df[["geoid10", "blank_bounds"]]

    census_tract = open_path("census_tract.geojson", "geoid10")

    df = pd.read_csv(data_path.joinpath("indicators_by_school_unscaled.csv"),
                      dtype={"School ID": str})
    df = pd.DataFrame(df)
    df = df.assign(college_ranked = pd.qcut(df.college_enroll_pct, 5, labels = [1, 2, 3, 4, 5]))

    fig = go.Figure()


    fig.add_trace(go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df["school_name"],
        marker_color=df['college_enroll_pct'],
        marker_cmin=min(df["college_enroll_pct"]),
        marker_cmax=max(df["college_enroll_pct"]),
        marker_colorbar=dict(thickness=20),
        marker_colorbar_title='College Enrollment Percentage',
        marker_colorscale='blues',
        marker_size=10,
        showlegend=False,
        visible=False))


    fig.update_traces(customdata=df["college_enroll_pct"])
    fig.update_traces(hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' +
                                    '<b>College Enrollment Percentage:</b> %{customdata}')


    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=census_df["geoid10"],
        z = census_df["blank_bounds"],
        showscale=False,
        hoverinfo='skip',
        visible=False
    ))

    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        title_text = 'College Enrollment by School',
        geo_scope='usa'
    )

    fig.update_coloraxes(showscale=False)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x unified')
    return fig
