from leuvenmapmatching.matcher.distance import DistanceMatcher
from leuvenmapmatching.map.inmem import InMemMap
from leuvenmapmatching import visualization as mmviz
import pandas as pd
import osmread
import geopandas
import traceback
from pyrosm import OSM
from pyrosm import get_data
import osmnx as ox

df = pd.read_csv('master_log.csv')
location = 'maryland'
ymin = df['jetson_rpi_lat'].max()
ymax = df['jetson_rpi_lat'].min()
xmin = df['jetson_rpi_lng'].max()
xmax = df['jetson_rpi_lng'].min()
print([xmin, ymin, xmax, ymax])
try:
  fp = get_data("maryland", update=False, directory='.')
  print('Loading OSM data...')
  osm = OSM(fp, bounding_box=[xmin, ymin, xmax, ymax])
  # osm = OSM('maryland-latest.osm.pbf', bounding_box=[xmin, ymin, xmax, ymax])
  print('Loading OSM data... done')
  print(osm)
  # Read all drivable roads
  # drive_net = osm.get_network(network_type="driving")
  # drive_net.to_file("maryland.shp")
  print('Extracting drivable roads...')
  # nodes, edges = osm.get_network(network_type="driving", nodes=True)
  G = ox.graph_from_bbox(ymax, ymin, xmax, xmin, network_type='drive', simplify=False, retain_all=True)
  nodes, edges = ox.graph_to_gdfs(G)
  print(nodes)
  print(edges)
  print('Extracting drivable roads... done')
  fig, ax = ox.plot_graph(ox.project_graph(G))
  fig.savefig('maryland.png')
  # edges.to_file("maryland_edges.shp")
  # G = ox.gdfs_to_graph(nodes, edges)
  # G = osm.to_graph(nodes, edges, graph_type="networkx")
  # print(G.nodes(data=True))
  # drive_net.show()
  # print(drive_net)
except:
  print(traceback.format_exc())

# map_con = InMemMap("mymap", graph={
#     "A": ((1, 1), ["B", "C", "X"]),
#     "B": ((1, 3), ["A", "C", "D", "K"]),
#     "C": ((2, 2), ["A", "B", "D", "E", "X", "Y"]),
#     "D": ((2, 4), ["B", "C", "F", "E", "K", "L"]),
#     "E": ((3, 3), ["C", "D", "F", "Y"]),
#     "F": ((3, 5), ["D", "E", "L"]),
#     "X": ((2, 0), ["A", "C", "Y"]),
#     "Y": ((3, 1), ["X", "C", "E"]),
#     "K": ((1, 5), ["B", "D", "L"]),
#     "L": ((2, 6), ["K", "D", "F"])
# }, use_latlon=False)
# geodf = geopandas.read_file(f"maryland.shp")
# get min and max coordinates of rpi route
#crop shape file to fit route
# cropped_map_data = geodf.cx[xmin:xmax, ymin:ymax]

# map_con = InMemMap(cropped_map_data, use_latlon=True, use_rtree=True, index_edges=True)
map_con = InMemMap("mymap", graph=G, use_latlon=False, index_edges=True, use_rtree=True)

# for entity in osmread.parse_file(cropped_map_data):
#     if isinstance(entity, osmread.Way) and 'highway' in entity.tags:
#         for node_a, node_b in zip(entity.nodes, entity.nodes[1:]):
#             map_con.add_edge(node_a, node_b)
#             map_con.add_edge(node_b, node_a)
#     if isinstance(entity, osmread.Node):
#         map_con.add_node(entity.id, (entity.lat, entity.lon))
# map_con.purge()

path = []

for index, row in df.iterrows():
    path.append((df['jetson_rpi_lat'].iloc[index], df['jetson_rpi_lng'].iloc[index]))

matcher = DistanceMatcher(map_con, max_dist=2, obs_noise=1, min_prob_norm=0.5, max_lattice_width=5)
states, _ = matcher.match(path)
nodes = matcher.path_pred_onlynodes

print("States\n------")
print(states)
print("Nodes\n------")
print(nodes)
print("")
matcher.print_lattice_stats()

mmviz.plot_map(map_con, matcher=matcher, show_labels=True, show_matching=True, show_graph=True, filename="my_plot.png")