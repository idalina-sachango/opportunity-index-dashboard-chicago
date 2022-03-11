import dash
from dash import dash_table
from dash import dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.express as px
import pathlib
import pandas as pd
import json
import scatter



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
### Dash App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("dashboard/datasets")

### datasets
### Data for table
df = pd.read_csv(DATA_PATH.joinpath('acs_data.csv'))
df = df[['NAME', 'tract', 'internet_rate', 'emp_rate_25_64', 'above_pov_rate']]  # prune columns for example


### Data for graph
geo_df = pd.read_csv(DATA_PATH.joinpath("School_Locations_SY1718.csv"), dtype={"COMMAREA": str})
geo_df = geo_df.fillna(999)

with open(DATA_PATH.joinpath("chicago-boundaries.geojson")) as f:
    jsn = json.load(f)

for i in range(len(jsn["features"])):
    jsn["features"][i]["id"] = jsn["features"][i]["properties"]["sec_neigh"]


### Map Choropleth Figure
fig = px.choropleth(geo_df, geojson=jsn, locations='COMMAREA', color='WARD_15',
                        color_continuous_scale="Viridis",
                        scope="usa", title = "School Opportunity Index"
                        )
fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

### App Title
app.title = "Tools4Schools"

### App Layout
app.layout = html.Div(
    children = [
        html.Div(
            children = [
            html.H1(children="Opportunity Index on College Outcomes",
                    className="header-title",),
            html.P(children = "Analyzes Chicago Public School performance on College Outcomes \
                            for the year 2017.",
                    className="header-description",),
            ],
            className="header",
        ),
        html.Div(
            children = [
                html.Div(
                    children = ['Map Title',
                        dcc.Graph(
                            id = 'Map Choropleth',
                            figure = fig),],
                    className="card",
                ),
                html.Div(
                    children = dash_table.DataTable(
                        columns=[
                            {'name': 'Census Tract', 'id': 'NAME', 'type': 'text'},
                            {'name': 'Tract ID', 'id': 'tract', 'type': 'numeric'},
                            {'name': '% Households with Internet subscription', 'id': 'internet_rate', 'type': 'numeric'},
                            {'name': 'Employment Rate for Individuals 25-64 years', 'id': 'emp_rate_25_64', 'type': 'numeric'},
                            {'name': '% Above Poverty Rate', 'id': 'above_pov_rate', 'type': 'numeric'}
                        ],
                        data=df.to_dict('records'),
                        filter_action='native',
                        style_table={
                            'height': 400,
                        },
                        style_data={
                            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        }
                    ),
                className="card",)
                ],
        className="wrapper",)
    ]
)

### Institute App callback to update when the index value is updated, eg graph with slider
# @app.callback(
#   Output('graph-with-slider', 'figure'),
#     [Input('month-slider', 'value')])
# def update_figure(selected_month):
#   filtered_df = df[df.month == selected_month]


#### Call the app
if __name__ == '__main__':
  app.run_server(host = '0.0.0.0', port = 5555, debug = False)