import plotly.graph_objects as go
from tools4schools.charts import scatter, college, poverty_rate, budget


def run_all():
    """
    Takes every chart object and adds them into a single
    plotly graph by adding their data as individual layers
    to the map. Creates buttons for each map where the user can toggle
    to a certain map view.
    Inputs: None
    Outputs: Plotly figure
    """

    scatter_fig = scatter.make_fig()
    college_fig = college.make_fig()
    poverty_fig = poverty_rate.make_fig()
    budget_fig = budget.make_fig()

    fig = go.Figure()

    fig.update_geos(fitbounds="locations", visible=True)
    fig.add_traces(scatter_fig.data)
    fig.add_traces(college_fig.data)
    fig.add_traces(poverty_fig.data)
    fig.add_traces(budget_fig.data)

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Opportunity Index by School",
                         method="update",
                         args=[{"visible": [True,True,True,
                                            True,True,True,
                                            False,False,False,
                                            False,False,False,
                                            False,False]}]),
                    dict(label="College Enrollment Percentage by School",
                         method="update",
                         args=[{"visible": [False,False,False,
                                            False,False,False,
                                            True,True,False,
                                            False,False,False,
                                            False,False]}]),
                    dict(label="Poverty Rate by Census Tract and College Enrollment by School",
                         method="update",
                         args=[{"visible": [False,False,False,
                                            False,False,False,
                                            False,False,True,
                                            True,False,False,
                                            False,False]}]),
                    dict(label="Budget by School",
                         method="update",
                         args=[{"visible": [False,False,False,
                                            False,False,False,
                                            False,False,False,
                                            False,True,True,
                                            True,True]}])
                ]),
                type = "buttons",
                direction="left",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.175,
                y=1.165,
                xanchor="left",
                yanchor="top"

            )

        ],
        font = dict(color='#000000')
    )

    fig.update_layout(template="plotly_white",margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#ffffff",
    hovermode='x unified')
    return fig