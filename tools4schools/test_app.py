
import dash
from dash import dcc
from dash import  html
from dash.dependencies import Input, Output
from tools4schools.charts import scatter, air_pollution


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
### Dash App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


### Figure 1
scatter_fig = scatter.make_fig()
air_pollution_fig = air_pollution.make_fig()


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
                    children = ['College enrollment by school',
                        dcc.Graph(
                            id = 'Map scatter',
                            figure = scatter_fig),],
                    className="card",
                ),
                ],
        className="wrapper",),
        html.Div(
            children = [
                html.Div(
                    children = ['Heat map of air pollution',
                        dcc.Graph(
                            id = 'Map choropleth',
                            figure = air_pollution_fig),],
                    className="card",
                ),
                ],
        className="wrapper",)
    ]
)

# ### Institute App callback to update when the index value is updated, eg graph with slider
# # @app.callback(
# #   Output('graph-with-slider', 'figure'),
# #     [Input('month-slider', 'value')])
# # def update_figure(selected_month):
# #   filtered_df = df[df.month == selected_month]


# #### Call the app
# if __name__ == '__main__':
#   app.run_server(host = '0.0.0.0', port = 5555, debug = False)