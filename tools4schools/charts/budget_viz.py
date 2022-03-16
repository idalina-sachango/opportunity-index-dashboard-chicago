import pandas as pd
import geopandas as gpd
#import matplotlib.pyplot as plt
#import plotly 
from pathlib import Path 
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np

#def make_fig():
home_path = Path(__file__).parent.parent 
data_path = home_path.joinpath("data/results")
data_path_geo = home_path.joinpath("data/geojson")

def open_path(filename, feature):
    with open(data_path_geo.joinpath(filename)) as f:
        df = json.load(f)
    for i in range(len(df["features"])):
        df["features"][i]["id"] = df["features"][i]["properties"][feature]
    return df

census_tract = open_path("census_tract.geojson", "geoid10")
census_df = gpd.read_file(data_path_geo.joinpath("census_tract.geojson"))
census_df["blank_bounds"] = 0
census_df = census_df[["geoid10", "blank_bounds"]]

fig = go.Figure()
df = pd.read_csv(data_path.joinpath("indicators_by_school_per_unit.csv"), dtype={"census_tract": str})
df = df.fillna(999)
df = pd.DataFrame(df)
df["blank_bounds"] = 0
df.rename(columns={"FY 2017 Ending Budget": "budget_per_student"}, inplace=True)


#create intervals for bubble size
# intervals = ["1000 - 10000", "10000 - 20000", "20000 - 30000", "30000 - 40000", "40000 - 50000"]
# tuple1 = (0, df[(df.budget_per_student > 1000) & (df.budget_per_student < 10000)].index[-1]+1)
# print("tuple1: ", tuple1)
# tuple2 = (tuple1[1], df[(df.budget_per_student >= 10000) & (df.budget_per_student < 20000)].index[-1]+1)
# print("tuple2: ", tuple2)
# tuple3 = (tuple2[1], df[(df.budget_per_student >= 20000) & (df.budget_per_student < 30000)].index[-1]+1)
# print("tuple3: ", tuple3)
# tuple4 = (tuple3[1], df[(df.budget_per_student >= 30000) & (df.budget_per_student < 40000)].index[-1]+1)
# print("tuple4: ", tuple4)
# tuple5 = (tuple4[1], df[(df.budget_per_student >= 40000) & (df.budget_per_student < 50000)].index[-1]+1)
# print("tuple5: ", tuple5)
# limits = [tuple1, tuple2, tuple3, tuple4]
# print("limits: ", limits)
# colors = ["#A1CAF1", "#6495ED", "#71A6D2", "#6082B6", "#0047AB"]

#create base census tract map
fig.add_trace(go.Choropleth(geojson=census_tract,featureidkey="properties.geoid10",
    locations=census_df["geoid10"],
    z = census_df["blank_bounds"],
    showscale=False,
))

fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x')

#create bubbles
#df["grouping"] = pd.cut(df["enrollment_crdc"], bins=list(range(0, 2000, 4000)), labels=["small", "medium", "large"])
colors = {"small": "#8F00FF", "medium": "#6495ED", "large": "#FFBF00"}
df['grouping'] = np.select(
    [
        df["enrollment_crdc"].between(0, 200, inclusive=False), 
        df["enrollment_crdc"].between(200, 1000, inclusive=False),
        df["enrollment_crdc"].between(1000, 5000, inclusive=False),
    ], 
    [
        'Small', 
        'Medium',
        'Large'
    ], 
    default='Unknown'
)
# for label in df["grouping"].unique():
#     df_sub = df[[df["grouping"] == label]]
# fig.add_trace(px.scatter_geo(df, locationmode = 'USA-states', size = "budget_per_student", 
# lon = "lon", lat = "lat", locations="ctfips", geojson = census_tract, featureidkey="properties.geoid10",
# text = "School Name"))

for _, row in df.iterrows():
    if row.grouping == "Small":
        shade = colors["small"]
    elif row.grouping == "Medium":
        shade = colors["medium"]
    else:
        row.grouping == "Large"
        shade = colors["large"]
    fig.add_trace(go.Scattergeo(
    lat = [row.latitude],
    lon = [row.longitude],
    showlegend = False,
    marker = dict(size = (row.budget_per_student) * 0.002,
    color = shade, 
    opacity = 0.5,
    line_color='rgb(40,40,40)', 
    line_width=0.5,
    sizemode = 'area'),
    text=pd.Series(row.school_name),
    customdata=pd.Series(round(row.budget_per_student, 2)),
    hovertemplate='<b>School Name<extra></extra></b>: %{text}<br>' + 
                                    '<b>Budget per Student:</b> %{customdata}',
    hoverinfo = "text"
    ))





#create bubbles raw
# budget_sum = df["budget_per_student"].sum()
# intervals_count = 0
# for i in range(len(limits)):
#    lim = limits[i]
#    df_sub = df[lim[0]:lim[1]]
#    fig.add_trace(go.Scattergeo(locationmode = 'USA-states', lon = df_sub['lon'],\
#    lat = df_sub['lat'],text = df_sub['School Name'], \
#    marker = dict(size = df_sub['budget_per_student']*0.002, color = colors[i], \
#    line_color='rgb(40,40,40)', line_width=0.5,sizemode = 'area'),\
#    name = '{}'.format(intervals[intervals_count])))
#    intervals_count += 1

# fig.update_layout(
#     title_text = "Budget Per Student",
#     title_x = 0.5,
#     show_legend = False,
#     # legend_title = "Budget per Student",
#     # geo = dict(
#     #     scope = 'usa',
#     #     landcolor = 'rgb(217, 217, 217)',
#     )
# fig.update_geos(fitbounds="locations", visible=True)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
# hovermode='x', title_text = 'Budget per Student',
# geo_scope='usa') 
fig.update_coloraxes(showscale=False)
fig.update_layout(
    legend=dict(
        x=0,
        y=1,
        traceorder="reversed",
        title_font_family="Times New Roman",
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
    )
)
#fig.update_traces(show_legend = False)
fig.show()
    #return fig







#census = json.load(data_path.joinpath("Boundaries - Census Tracts - 2010.geojson")
#px.choropleth(geojson=census, featureidkey="properties.geoid10")

#df = pd.read_csv(data_path.joinpath("budget_viz_data.csv"))
#budgets_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude_x, df.latitude_x))
#px.scatter_geo(budgets_gdf, budgets_gdf.longitude_x, budgets_gdf.latitude_x)
#print(df.head())
#print(budgets_gdf.head())
#print(geo_json.head())