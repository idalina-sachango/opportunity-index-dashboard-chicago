import flask
from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd

# def shapefile2geojson(infile, outfile, fieldname):
#     '''Translate a shapefile to GEOJSON.'''
#     options = gdal.VectorTranslateOptions(format="GeoJSON",
#                                           dstSRS="EPSG:4326")
#     gdal.VectorTranslate(outfile, infile, options=options)


app = Flask(__name__)
@app.route("/", methods=["GET"])
def status():
    print("/")
    return "Status: OK"

# @app.route("/map", methods=["GET"])
# def map():
#     print("/map")
#     return render_template("map_chicago.html")
#     # return(my_map.get_root().render())

def index():
    chicago = [41.8781136, -87.6297982]
    chi_sd = gpd.read_file('data/tl_2017_17_tract.zip')
    map_chicago = folium.Map(location=chicago, zoom_start=8)
    
    for _, r in chi_sd.iterrows():
    # Without simplifying the representation of each borough,
    # the map might not be displayed
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                            style_function=lambda x: {'fillColor': 'orange'})
        folium.Popup(r['NAME']).add_to(geo_j)
        geo_j.add_to(map_chicago)

    map_chicago.save("templates/map_chicago.html")

if __name__=="__main__":
    index()
    print("Map is generated")

    app.run(host="0.0.0.0", port=5500, debug=True)