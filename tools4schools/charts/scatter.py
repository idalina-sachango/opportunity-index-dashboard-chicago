
import plotly.graph_objects as go
import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path


def make_fig():
    home_path = Path(__file__).parent.parent
    data_path = home_path.joinpath("data")
    data_path_geo = home_path.joinpath("data/geojson")
    

    bounds_chi = pd.read_csv(data_path.joinpath("cps-comarea-bounds.csv"), dtype={"Zip": str})

    # zipcodes geo
    with open(data_path_geo.joinpath("zipcodes.geojson")) as f:
        coms = json.load(f)
    for i in range(len(coms["features"])):
        coms["features"][i]["id"] = coms["features"][i]["properties"]["zip"]

    # cps location geo
    with open(data_path_geo.joinpath("cps-geojson.geojson")) as f:
        jsn = json.load(f)
    for i in range(len(jsn["features"])):
        jsn["features"][i]["id"] = jsn["features"][i]["properties"]["school_id"]

    # census tract geo
    with open(data_path_geo.joinpath("census_tract.geojson")) as f:
        census = json.load(f)
    for i in range(len(jsn["features"])):
        census["features"][i]["id"] = census["features"][i]["properties"]["geoid10"]

    cps_bounds = json_normalize(jsn["features"])
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
    r, col = full.shape
    sm = sum(full["grad17"])

    # plot bubbles with cps college data
    for row in full.itertuples():
        fig.add_trace(go.Scattergeo(
        lon = [row[63]],
        lat = [row[66]],
        fill=True,
        fillcolor='purple',
        marker = dict(
                size = row[16]/30,
                line_color='purple',
                line_width=0.5,
                sizemode = 'area'
            )
        ))

    # draw census tract boundaries
    fig.add_trace(go.Choropleth(
        geojson=census,
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
