import geopandas as gpd
from shapely.geometry import Polygon
import folium
import pandas as pd

df = pd.read_csv('master_log.csv')

lat_point_list = df['jetson_rpi_lat'].tolist()
lon_point_list = df['jetson_rpi_lng'].tolist()

polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
crs = {'init': 'epsg:4326'}
polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       

polygon.to_file(filename='polygon.geojson', driver='GeoJSON')
polygon.to_file(filename='polygon.shp', driver="ESRI Shapefile")
m = folium.Map([50.854457, 4.377184], zoom_start=5, tiles='cartodbpositron')
folium.GeoJson(polygon).add_to(m)
folium.LatLngPopup().add_to(m)
m.save('polygon.html')