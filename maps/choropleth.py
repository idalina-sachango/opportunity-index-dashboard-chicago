import json
import plotly.express as px
import pandas as pd
from urllib.request import urlopen

df = pd.read_csv("data/School_Locations_SY1718.csv", dtype={"COMMAREA": str})
df = df.fillna(999)

with open("data/chicago_boundaries.geojson") as f:
    jsn = json.load(f)

for i in range(len(jsn["features"])):
    jsn["features"][i]["id"] = jsn["features"][i]["properties"]["community"]

print(px.data.election().keys())
print(px.data.election_geojson())


fig = px.choropleth(df, geojson=jsn, locations='COMMAREA', color='WARD_ADJ',
                           color_continuous_scale="Viridis",
                           scope="usa"
                          )
fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()