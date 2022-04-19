import geopandas as gpd
from shapely.geometry import Polygon, LineString
import folium
import pandas as pd

df = pd.read_csv('master_log.csv')

lat_point_list = df['jetson_rpi_lat'].tolist()
lon_point_list = df['jetson_rpi_lng'].tolist()

polygon_geom = LineString(zip(lon_point_list, lat_point_list))
crs = {'init': 'epsg:4326'}
polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       

polygon.to_file(filename='polygon.geojson', driver='GeoJSON')
polygon.to_file(filename='polygon.shp', driver="ESRI Shapefile")
m = folium.Map([df['jetson_rpi_lat'][0], df['jetson_rpi_lng'][0]], zoom_start=5, tiles='cartodbpositron')
folium.GeoJson(polygon).add_to(m)
folium.LatLngPopup().add_to(m)
m.save('polygon.html')