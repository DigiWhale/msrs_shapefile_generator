from fmm import Network,NetworkGraph,STMATCH,STMATCHConfig


def load_network(shapefile):
  network = Network(shapefile)
  print(f"Nodes {network.get_node_count()} edges {network.get_edge_count()}")
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

model = create_model(load_network('polygon.shp'), create_graph(load_network('polygon.shp')))
stmatch_config = set_config()
wkt = "LINESTRING(0.200812146892656 2.14088983050848,1.44262005649717 2.14879943502825,3.06408898305084 2.16066384180791,3.06408898305084 2.7103813559322,3.70872175141242 2.97930790960452,4.11606638418078 2.62337570621469)"
result = model.match_wkt(wkt,stmatch_config)
print(result.mgeom.export_wkt())