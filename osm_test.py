import osmnx as ox
G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
ox.plot_graph(ox.project_graph(G), filename = "plot.png", show = False, save = True, close = True)