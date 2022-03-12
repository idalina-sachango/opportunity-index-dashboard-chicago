from dash import Dash, dash_table
import dash_leaflet as dl
from dash.dependencies import Input, Output
import flask
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import pandas as pd


server_app = Flask(__name__)


map_app = Dash(__name__, server=server_app, url_base_pathname='/map/')
map_app.layout = dl.Map(dl.TileLayer(), style={'height': '100vh'})



df = pd.read_csv('../data/acs_data.csv')
df = df[['NAME', 'tract', 'internet_rate', 'emp_rate_25_64', 'above_pov_rate']]  # prune columns for example

table_app = Dash(__name__, server=server_app, url_base_pathname='/table/')
table_app.layout = dash_table.DataTable(
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
)
@server_app.route('/')

@server_app.route('/table/')
def render_table():
    return flask.redirect('/table/')


@server_app.route('/map/')
def render_map():
    return flask.redirect('/map/')

run_app = DispatcherMiddleware(server_app, {
    '/table/': table_app.server,
    '/map/': map_app.server
})

run_simple('0.0.0.0', 5555, run_app, use_reloader=False, use_debugger=False)

