import json
import plotly.express as px
import pandas as pd
from urllib.request import urlopen

df = pd.DataFrame(pd.read_csv("data/School_Locations_SY1718.csv", dtype={"School_ID": str}))
df = df[["School_ID", "the_geom","Lat", "Long", "WARD_15"]]
df = df.fillna(999)
df = df.astype({"School_ID": int, "Lat": int, "Long": int, "WARD_15": str})

with open("data/cps-1718.geojson") as f:
    jsn = json.load(f)
    print(jsn["features"][0]["properties"]["school_id"])

for i in range(len(jsn["features"])):
    jsn["features"][i]["id"] = jsn["features"][i]["properties"]["school_id"]

fig = px.choropleth(df, geojson=jsn,
                           locations='School_ID',
                           color="WARD_15"
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

