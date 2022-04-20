import osmnx as ox
G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
ox.plot_graph(G, save=True, file_format='svg')