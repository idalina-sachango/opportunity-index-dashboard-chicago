from dash import Dash, dash_table
from dash.dependencies import Input, Output
from flask import Flask

import pandas as pd
import pathlib


# relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets")

df = pd.read_csv(DATA_PATH.joinpath('acs_data.csv'))
df = df[['NAME', 'tract', 'internet_rate', 'emp_rate_25_64', 'above_pov_rate']]  # prune columns for example


#table_app = Dash(__name__, sharing=True, server=server)
layout = dash_table.DataTable(
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
