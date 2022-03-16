import pandas as pd
import geopandas as gpd
#import matplotlib.pyplot as plt
#import plotly 
from pathlib import Path 
import plotly.express as px
import plotly.graph_objects as go
import json


home_path = Path(__file__).parent.parent 
data_path = home_path.joinpath("Project/Output")
data_path_geo = home_path.joinpath("data")



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
df = pd.read_csv(data_path.joinpath("indicators_by_school_scaled.csv"), dtype={"census_tract_x": str})
df = df.fillna(999)
df = pd.DataFrame(df)
df["blank_bounds"] = 0
df.rename(columns={"FY 2017 Ending Budget": "budget_per_student", "census_tract_x": "ctfips", \
"latitude_x": "lat", "longitude_x": "lon", "School Name": "school_name"}, inplace=True)
#print(df[df["School Name"] == "VAUGHN HS"])


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
    z = census_df["blank_bounds"]
))

fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hovermode='x')

#create bubbles
# df["grouping"] = pd.cut(df["budget_per_student"], bins=list(range(0, 60000, 10000)), labels=["a", "b", "c", "d", "e"])
# for label in df["grouping"].unique():
#     df_sub = df[[df["grouping"] == label]]
# fig.add_trace(px.scatter_geo(df, locationmode = 'USA-states', size = "budget_per_student", 
# lon = "lon", lat = "lat", locations="ctfips", geojson = census_tract, featureidkey="properties.geoid10",
# text = "School Name"))

for _, row in df.iterrows():
    budge = pd.Series(row.budget_per_student)
    fig.add_trace(go.Scattergeo(
    lat = [row.lat],
    lon = [row.lon],
    marker = dict(size = (row.budget_per_student) * 0.002,
    color = 'rgb(93, 164, 214)', 
    line_color='rgb(40,40,40)', 
    line_width=0.5,
    sizemode = 'area'),
    text=pd.Series(row.school_name),
    customdata=pd.Series(row.budget_per_student),
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
#fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(title_text='Budget Per Student', title_x=0.5)
#fig.update_layout(title_text = "Budget Per Student", show_legend=False, geo_scope='usa')
fig.show()







#census = json.load(data_path.joinpath("Boundaries - Census Tracts - 2010.geojson")
#px.choropleth(geojson=census, featureidkey="properties.geoid10")

#df = pd.read_csv(data_path.joinpath("budget_viz_data.csv"))
#budgets_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude_x, df.latitude_x))
#px.scatter_geo(budgets_gdf, budgets_gdf.longitude_x, budgets_gdf.latitude_x)
#print(df.head())
#print(budgets_gdf.head())
#print(geo_json.head())