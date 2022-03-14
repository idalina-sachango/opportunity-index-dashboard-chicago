
import plotly.graph_objects as go
import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path


def make_fig():
    home_path = Path(__file__).parent.parent
    data_path = home_path.joinpath("data")
    data_path_geo = home_path.joinpath("data/geojson")


    def open_path(filename, feature):
        with open(data_path_geo.joinpath(filename)) as f:
            df = json.load(f)
        for i in range(len(df["features"])):
            df["features"][i]["id"] = df["features"][i]["properties"][feature]
        return df

    cps_locations = open_path("cps-geojson.geojson", "school_id")
    census_tract = open_path("census_tract.geojson", "geoid10")


    cps_bounds = json_normalize(cps_locations["features"])
    coords = 'geometry.coordinates'
    df = (cps_bounds[coords].apply(lambda r: [(r[0],r[1])])
            .apply(pd.Series).stack()
            .reset_index(level=1).rename(columns={0:coords,"level_1":"point"})
            .join(cps_bounds.drop(coords,1), how='left')).reset_index(level=0)
    df[['lat','long']] = df[coords].apply(pd.Series)

    df = pd.DataFrame(df)
    df = df.rename(columns={"properties.school_id": "schoolid"})
    df = df.astype({"id": str})


    df2 = pd.read_csv(data_path.joinpath("college.csv"), dtype={"schoolid": str})
    df2 = df2.fillna(999)
    df2 = pd.DataFrame(df2)

    #merge cps college data with csv with latitude longitude for schools
    full = pd.merge(df2, df, on='schoolid',  how='left')

    df3 = pd.read_csv(data_path.joinpath("chi_air.csv"), dtype={"ctfips": str})
    df3 = df3.fillna(999)
    df3 = pd.DataFrame(df3)
    df3["blank_bounds"] = 0

    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    fig = go.Figure()

    #plot bubbles with cps college data
    for _, row in full.iterrows():
        fig.add_trace(go.Scattergeo(
        lon = [row['properties.long']],
        lat = [row['properties.lat']],
        marker = dict(
            #size=row['pctenroll17']/100,
            # line_color='rgb(40,40,40)',
            # line_width=0.5,
            # sizemode = 'area'
            color=row['pctenroll17']/100,
            colorscale=["blue", "red"] 
        )))

    # draw census tract boundaries
    fig.add_trace(go.Choropleth(
        geojson=census_tract,
        featureidkey="properties.geoid10",
        locations=df3["ctfips"],
        z = df3["blank_bounds"]
    ))

    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_layout(
        title_text = 'College Enrollment by School',
        geo_scope='usa', # limite map scope to USA
    )

    return fig
