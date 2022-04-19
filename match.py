from fmm import Network,NetworkGraph,STMATCH,STMATCHConfig
import osmnx as ox
import time
from shapely.geometry import Polygon
import os

def save_graph_shapefile_directional(G, filepath=None, encoding="utf-8"):
    # default filepath if none was provided
    if filepath is None:
        filepath = os.path.join(ox.settings.data_folder, "graph_shapefile")

    # if save folder does not already exist, create it (shapefiles
    # get saved as set of files)
    if not filepath == "" and not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath_nodes = os.path.join(filepath, "nodes.shp")
    filepath_edges = os.path.join(filepath, "edges.shp")

    # convert undirected graph to gdfs and stringify non-numeric columns
    gdf_nodes, gdf_edges = ox.utils_graph.graph_to_gdfs(G)
    gdf_nodes = ox.io._stringify_nonnumeric_cols(gdf_nodes)
    gdf_edges = ox.io._stringify_nonnumeric_cols(gdf_edges)
    # We need an unique ID for each edge
    gdf_edges["fid"] = gdf_edges.index
    # save the nodes and edges as separate ESRI shapefiles
    gdf_nodes.to_file(filepath_nodes, encoding=encoding)
    gdf_edges.to_file(filepath_edges, encoding=encoding)

print("osmnx version",ox.__version__)
bounds = (18.029122582902115, 18.070836297501724, 59.33476653724975, 59.352622230576124)
x1,x2,y1,y2 = bounds
boundary_polygon = Polygon([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])
G = ox.graph_from_polygon(boundary_polygon, network_type='drive')
start_time = time.time()
save_graph_shapefile_directional(G, filepath='./stockholm')
print("--- %s seconds ---" % (time.time() - start_time))

def load_network(shapefile):
  network = Network(shapefile)
  # print(f"Nodes {network.get_node_count()} edges {network.get_edge_count()}")
  return network

def create_graph(network):
  graph = NetworkGraph(network)
  return graph

def create_model(network, graph):
  model = STMATCH(network,graph)
  return model

def set_config():
  k = 4
  gps_error = 0.5
  radius = 0.4
  vmax = 30
  factor = 1.5
  stmatch_config = STMATCHConfig(k, radius, gps_error, vmax, factor)
  return stmatch_config

# model = create_model(load_network('polygon.shp'), create_graph(load_network('polygon.shp')))
# stmatch_config = set_config()
# wkt = "LINESTRING(0.200812146892656 2.14088983050848,1.44262005649717 2.14879943502825,3.06408898305084 2.16066384180791,3.06408898305084 2.7103813559322,3.70872175141242 2.97930790960452,4.11606638418078 2.62337570621469)"
# result = model.match_wkt(wkt,stmatch_config)
# print(result.mgeom.export_wkt())