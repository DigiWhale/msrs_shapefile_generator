import osmnx as ox
G = ox.graph_from_bbox(38.68130169804593, 38.38845630130091, -76.43606009382191, -76.63372100194263, network_type='drive')
fig, ax = ox.plot_graph(ox.project_graph(G))
fig.savefig('maryland.png')