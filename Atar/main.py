#------------------------------------------------------------------------------
#	Libraries
#------------------------------------------------------------------------------
from time import sleep
from shutil import rmtree
import os

from map import Map
from search import Astar


#------------------------------------------------------------------------------
#   Output directory
#------------------------------------------------------------------------------
OUT_DIR = "output/"

rmtree(OUT_DIR)
os.makedirs(OUT_DIR)


#------------------------------------------------------------------------------
#	Main execution
#------------------------------------------------------------------------------
# Create an instance of map
barrier = [
	(15,15), (15,14), (15,13), (15,12), (15,11), (15,10), (15,9), (15,8),
	(15,15), (14,15), (13,15), (12,15), (11,15), (10,15), (9,15), (8,15),

	(14,15), (14,14), (14,13), (14,12), (14,11), (14,10), (14,9), (14,8),
	(15,14), (14,14), (13,14), (12,14), (11,14), (10,14), (9,14), (8,14),
]
Map_obj = Map(height=25, width=25, barrier=barrier)


# Create an instance of A* search algorithm
cost_weight = {"g": 0.5, "h": 1.0}
Astar_obj = Astar(map_matrix=Map_obj.map, lamda=cost_weight)


# Search the shortest path
start = (0,0)
stop = (24,24)
shortest_path = Astar_obj.search_shortest_path(start=start, stop=stop)
print("Number of point:", len(shortest_path))


# Visualize map
path = []
for point_idx, point in enumerate(shortest_path):
	path.append(point)
	output_file = "output/%d.png" % (point_idx)
	Map_obj.visualize_map(start=start, stop=stop, path=path, savename=output_file)