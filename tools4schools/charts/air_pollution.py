import plotly.graph_objects as go
import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path


def make_fig():
    home_path = Path(__file__).parent.parent
    data_path = home_path.joinpath("data")
    data_path_geo = home_path.joinpath("data/geojson")


    with open(data_path_geo.joinpath("census_tract.geojson")) as f:
        jsn = json.load(f)
    for i in range(len(jsn["features"])):
        jsn["features"][i]["id"] = jsn["features"][i]["properties"]["geoid10"]


    df2 = pd.read_csv(data_path.joinpath("chi_air.csv"), dtype={"ctfips": str})
    df2 = df2.fillna(999)
    df2 = pd.DataFrame(df2)

    fig = go.Figure()

    fig.add_trace(go.Choropleth(
            geojson=jsn,
            featureidkey="properties.geoid10",
            locations=df2["ctfips"],
            z = df2["ds_pm_pred"],
            autocolorscale=True,
            showscale = False
        ))

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_layout(
        title_text = 'Air Quality By Census Tract',
        geo_scope='usa', # limite map scope to USA
    )

    return fig
