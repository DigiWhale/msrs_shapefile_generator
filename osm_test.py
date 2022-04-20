import osmnx as ox
G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
fig, ax = ox.plot_graph(ox.project_graph(G))
fig.savefig('maryland.png')