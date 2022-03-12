from dash import dcc, html, Input, Output, callback
import json
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import app
import pathlib


# relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets")

df = pd.read_csv(DATA_PATH.joinpath("School_Locations_SY1718.csv"), dtype={"COMMAREA": str})
df = df.fillna(999)


with open(DATA_PATH.joinpath("chicago-boundaries.geojson")) as f:
    jsn = json.load(f)

print(jsn["features"][0]["properties"])
for i in range(len(jsn["features"])):
    jsn["features"][i]["id"] = jsn["features"][i]["properties"]["sec_neigh"]


layout = html.Div([
    html.H1('Chicago Districts', style={"textAlign": "center"}),

    # html.Div([
    #     html.Div(dcc.Dropdown(
    #         id='genre-dropdown', value='Strategy', clearable=False,
    #         options=[{'label': x, 'value': x} for x in sorted(df.Genre.unique())]
    #     ), className='six columns'),

    #     html.Div(dcc.Dropdown(
    #         id='sales-dropdown', value='EU Sales', clearable=False,
    #         persistence=True, persistence_type='memory',
    #         options=[{'label': x, 'value': x} for x in sales_list]
    #     ), className='six columns'),
    # ], className='row'),

    dcc.Graph(id='my-bar', figure={}),
])

@callback(
    Output(component_id='my-bar', component_property='figure')
)

def display_choropleth():
    fig = px.choropleth(df, geojson=jsn, locations='COMMAREA', color='WARD_15',
                            color_continuous_scale="Viridis",
                            scope="usa"
                            )
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig