from leuvenmapmatching.matcher.distance import DistanceMatcher
from leuvenmapmatching.map.inmem import InMemMap
from leuvenmapmatching import visualization as mmviz
import pandas as pd

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
df = pd.read('master_log.csv')

map_con = InMemMap("../maryland-latest.osm.pbf", use_latlon=True)

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