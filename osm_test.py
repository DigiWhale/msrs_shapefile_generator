import osmnx as ox
G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
fig, ax = ox.plot_graph(G, save=True, show=False, filename='image', file_format='svg')