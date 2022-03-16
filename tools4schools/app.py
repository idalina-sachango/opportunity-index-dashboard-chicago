'''
Dash App for Tools4Schools

Output layout including 3 visulations and a table of
the resulting data using callbacks
'''
from pathlib import Path
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import flask
import pandas as pd
import dash
from tools4schools.charts import run_all, enroll_scatter


def generate_table(dataframe):
    '''
    Creates a Dash Datatable to output on the dash App with the school's
    opportunity index and a variety of indicators.

    Inputs:
        dataframe (pandas df): dataframe

    Returns: dashtable
    '''
    table = dash_table.DataTable(data=dataframe.to_dict('records'),
            columns=[
            {'name': 'School Name', 'id': 'school_name', 'type': 'text'},
            {'name': 'Census Tract', 'id': 'census_tract', 'type': 'numeric'},
            {'name': 'Opportunity Index', 'id': 'opportunity_index',
                    'type': 'numeric'},
            {'name': 'Student Enrollment', 'id': 'enrollment_crdc',
                'type': 'numeric'},
            {'name': '% College enrollment', 'id': 'college_enroll_pct',
                'type': 'numeric'},
            {'name': 'Free or Reduced Price Lunch',
                'id': 'free_or_reduced_price_lunch', 'type': 'numeric'},
            {'name': '# Certified Teachers',
                'id': 'teachers_certified_fte_crdc', 'type': 'numeric'},
            {'name': '# Counselors', 'id': 'counselors_fte_crdc',
                'type': 'numeric'},
            {'name': '# Law Enforcement Officers',
                'id': 'law_enforcement_fte_crdc', 'type': 'numeric'},
            {'name': 'Average Salaries', 'id': 'salaries_crdc',
                'type': 'numeric'},
            {'name': '# Students Enrolled in AP courses', 'id': 'enrl_AP_crdc',
                    'type': 'numeric'},
            {'name': 'FY 2017 Ending Budget', 'id': 'FY 2017 Ending Budget',
                'type': 'numeric'},
            {'name': '% Households with Internet subscription',
                'id': 'internet_rate', 'type': 'numeric'},
            {'name': 'Employment Rate for Individuals 25-64 years',
                'id': 'emp_rate_25_64', 'type': 'numeric'},
            {'name': '% Above Poverty Rate', 'id': 'above_pov_rate',
                'type': 'numeric'},
            {'name': '% Households on Food Stamps', 'id': 'food_stamps',
                'type': 'numeric'},
            {'name': 'Median Household Income', 'id': 'median_earnings',
                'type': 'numeric'}
            ],
            style_table={'height': 400,'overflowX': 'auto',},
            style_data={
                        'width': '150px', 'minWidth': '150px',
                        'maxWidth': '150px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
            page_size=10)
    return table

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

server = flask.Flask(__name__)
### Dash App
app = dash.Dash(__name__, server = server,
            external_stylesheets=external_stylesheets)


### Figures
run_all_fig = run_all.run_all()
enroll_scatter_fig = enroll_scatter.make_fig()


### Table Data
home_path = Path(__file__).parent
data_path = home_path.joinpath("data/results")
df1 = pd.read_csv(data_path.joinpath('opportunity_index_by_school_scaled.csv'))
df2 = pd.read_csv(data_path.joinpath('indicators_by_school_unscaled.csv'))
df2['college_enroll_pct'] = df2['college_enroll_pct']*100

merged_df = pd.merge(df1[['opportunity_index', 'ncessch',
                            'enrollment_crdc']],
                    df2, how='left')

table_df = merged_df[['school_name', 'census_tract', 'opportunity_index',
       'college_enroll_pct', 'free_or_reduced_price_lunch',
       'teachers_certified_fte_crdc', 'counselors_fte_crdc',
       'law_enforcement_fte_crdc', 'salaries_crdc', 'enrl_AP_crdc',
       'enrollment_crdc', 'above_pov_rate', 'internet_rate', 'emp_rate_25_64',
       'FY 2017 Ending Budget', 'food_stamps', 'median_earnings',
       'ds_pm_pred']]




### App Title
app.title = "Tools4Schools"

### App Layout
app.layout = html.Div(
    children = [
        html.Div(
            children = [
            html.H1(children="Opportunity Index on College Outcomes",
                    className="header-title",),
            html.P(children = "Analyzes Chicago Public Schools High School performance on \
                            College Outcomes for the year 2017.",
                    className="header-description",),
            ],
            className="header",
        ),
        html.Div(
            children = [
                html.Div(
                    children = [
                        dcc.Graph(
                            id = 'Maps',
                            figure = run_all_fig),],
                    className="row",),
                html.Div(
                    children=[
                            html.H3("Opportunity Index and College Enrollment for \
                            Chicago High Schools in 2017"),
                            dcc.Graph(
                            id = 'enroll-scatter',
                            figure = enroll_scatter_fig),],
                    className="row",
                ),
                ],
        className="row",),
        html.Div(
                dcc.Dropdown(id='dropdown',
                            options=[{'label': i, 'value': i} \
                                for i in table_df['school_name'].unique()],
                            multi=True,
                            placeholder='Filter by School name...',),
                                            ),
        html.Div(id='table-container')
    ]
)


### Dropdown callback for DataTable
@app.callback(Output('table-container', 'children'),
    [Input('dropdown', 'value')])

def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(table_df)

    dff = table_df[table_df.school_name.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)