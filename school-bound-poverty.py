import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

polygons = gpd.read_file("data/cps_21/geo_export_fbc23527-5232-4822-9a45-7f52a3b28f07.shp")
print(polygons)
polygon_id_field = 'id'
points = gpd.read_file("data/school_location_shape_21/geo_export_2f4a195e-ffbf-4775-a8f2-5ed70397929a.shp")

sjoin = gpd.sjoin(polygons, points, how='left', op='intersects')
count = sjoin.groupby(polygon_id_field)[polygon_id_field].count()
count.name='pointcount'
polygons = pd.merge(left=polygons, right=count, left_on=polygon_id_field, right_index=True)

fig, ax = plt.subplots(figsize = (10,8))
polygons.plot(column = 'pointcount', cmap = 'Purples', ax=ax, legend=True, 
              legend_kwds={'label':'Number of sites with ancient remains'})
polygons.geometry.boundary.plot(color=None, edgecolor='k',linewidth = 1, ax=ax)