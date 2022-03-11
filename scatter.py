import plotly.graph_objects as go
import pandas as pd
import json
from pandas.io.json import json_normalize

bounds_chi = pd.read_csv("data/cps-comarea-bounds.csv", dtype={"Zip": str})

with open("data/zipcodes.geojson") as f:
    coms = json.load(f)
for i in range(len(coms["features"])):
    coms["features"][i]["id"] = coms["features"][i]["properties"]["zip"]


with open("data/cps-geojson.geojson") as f:
    jsn = json.load(f)
for i in range(len(jsn["features"])):
    jsn["features"][i]["id"] = jsn["features"][i]["properties"]["school_id"]



cps_bounds = json_normalize(jsn["features"])
coords = 'geometry.coordinates'

df = (cps_bounds[coords].apply(lambda r: [(r[0],r[1])])
           .apply(pd.Series).stack()
           .reset_index(level=1).rename(columns={0:coords,"level_1":"point"})
           .join(cps_bounds.drop(coords,1), how='left')).reset_index(level=0)
df[['lat','long']] = df[coords].apply(pd.Series)

df = pd.DataFrame(df)
df = df.rename(columns={"properties.school_id": "schoolid"})
df = df.astype({"id": str})


df2 = pd.read_csv("data/college.csv", dtype={"schoolid": str})
df2 = df2.fillna(999)
df2 = pd.DataFrame(df2)

full = pd.merge(df2, df, on='schoolid',  how='left')
print(full.columns)
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
fig = go.Figure()
r, col = full.shape
sm = sum(full["grad17"])
print(sm)

for row in full.itertuples():
    fig.add_trace(go.Scattergeo(
    lon = [row[63]],
    lat = [row[66]],
    marker = dict(
            #size = row[16]/30,
            color="red",
            line_color='rgb(40,40,40)',
            line_width=0.5,
            #sizemode = 'area'
        )
    ))

fig.add_trace(go.Choropleth(
        geojson=coms,
        featureidkey="properties.zip",
        locations=bounds_chi["Zip"],
        z = full["grad17"],
        autocolorscale=True,
        showscale = False
    ))

fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.update_layout(
    title_text = 'College Enrollment by School',
    geo_scope='usa', # limite map scope to USA
)

fig.show()
