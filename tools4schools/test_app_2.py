from select import select
import dash
from dash import dash_table
from dash import dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.express as px
import pathlib
import pandas as pd
import json


# relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("dashboard/datasets")

### datasets
### Data for table
df = pd.read_csv(DATA_PATH.joinpath('acs_data.csv'))
df = df[['NAME', 'tract', 'internet_rate', 'emp_rate_25_64', 'above_pov_rate']]  # prune columns for example


### Initialize App

app = dash.Dash(__name__)
app.title = 'Tools4Schools'
#max_y = max(df['above_pov_rate'])
fig_1 = px.scatter(df, x='internet_rate', y='above_pov_rate', 
                    color='tract', template='plotly_dark')
fig_1 = fig_1.update_yaxes(range=[0, 100])
fig_1 = fig_1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

### Table
table1 = dash_table.DataTable(id='table',
                            data=df.to_dict('records'),
                            columns=[
                            {'name': 'Census Tract', 'id': 'NAME', 'type': 'text'},
                            {'name': 'Tract ID', 'id': 'tract', 'type': 'numeric'},
                            {'name': '% Households with Internet subscription', 'id': 'internet_rate', 'type': 'numeric'},
                            {'name': 'Employment Rate for Individuals 25-64 years', 'id': 'emp_rate_25_64', 'type': 'numeric'},
                            {'name': '% Above Poverty Rate', 'id': 'above_pov_rate', 'type': 'numeric'}
                        ],
                        filter_action='native',
                        style_table={
                            'height': 400,
                        },
                        style_data={
                            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },
                        style_header={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },
                        page_size=6,
                        page_action='native',
                        virtualization=True
                    )

def get_options(lst_names):
    dict_list = []
    for i in lst_names:
        dict_list.append({'label': i, 'value': i})

    return dict_list


final_table = html.Div(id="final_table")
# Define the app
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls',
                                            children=[
                                                html.H2('Tools4Schools'),
                                                html.P('''Visualizing Opportunity and College acceptances'''),
                                                html.P('''Pick one or more census tract from the dropdown below.'''),
                                                dcc.Dropdown(id='schoolselect',
                                                                options=get_options(df['NAME'].unique()),
                                                                multi=True,
                                                                value=[df['NAME'].sort_values()[0]],
                                                                style={'backgroundColor': 'rgb(50, 50, 50)',
                                                                        'color': 'white'},
                                                                className='schoolselect'),
                                            ]),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey',
                                           children=[dcc.Graph(id='scatterplot',
                                                    config={'displayModeBar': False},
                                                    animate=True,
                                                    figure=fig_1
                                                    ),
                                                    table1,
                                                    # dash_table.DataTable(
                                                    #     id = "table-container",
                                                    #     columns = [
                                                    #     {'name': 'Census Tract', 'id': 'NAME', 'type': 'text'},
                                                    #     {'name': 'Tract ID', 'id': 'tract', 'type': 'numeric'},
                                                    #     {'name': '% Households with Internet subscription', 'id': 'internet_rate', 'type': 'numeric'},
                                                    #     {'name': 'Employment Rate for Individuals 25-64 years', 'id': 'emp_rate_25_64', 'type': 'numeric'},
                                                    #     {'name': '% Above Poverty Rate', 'id': 'above_pov_rate', 'type': 'numeric'}
                                                    # ], data = df.to_dict('records'),
                                                    # row_deletable=True
                                                    # 
                                                    ],
                                                ),
                                           ])
                                 ]  # Define the right element
                            )


@app.callback(
   dash.dependencies.Output('table-container', 'data'),
   [dash.dependencies.Input('schoolselect', 'value')]
   )
def update_rows(selected_rows):
    """Filter df, return rows that match my_key"""
    dff = df[df['NAME'] == selected_rows]

    return [dff.to_dict('records')]
                        
       

# def on_trace_click(click_data):
#     """Listen to click events and update table, passing filtered rows"""
#     p = trace_click['points'][0]

#     # here, use 'customdata' property of clicked point, 
#     # could also use 'curveNumber', 'pointIndex', etc.
#     if 'customdata' in p:
#         key = p['customdata']['my-key']

#     df_f = get_corresponding_rows(df, key)

#     return df_f.to_dict('records')




# Run the app
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port = 5555, debug = False)