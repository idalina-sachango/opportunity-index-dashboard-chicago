
### Landing Page for the App

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to our app pages
from apps import table_app, map_app

app.layout = html.Div([
    html.Div([
        dcc.Link('Data Table |', href = '/apps/table_app'),
        dcc.Link(' Map Visualizations', href = '/apps/map_app')
    ], className = "row"),
    dcc.Location(id="url", refresh=False),
    html.Div(id='page-content', children=[])
])

@app.callback(Output(component_id='page-content', component_property='children'),
            [Input(component_id='url', component_property='pathname')])

def display_page(pathname):
    if pathname == '/apps/table_app':
        return table_app.layout
    if pathname == '/apps/map_app':
        return map_app.layout
    else:
        return "404 PAGE ERROR! Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=True)