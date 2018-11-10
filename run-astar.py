#------------------------------------------------------------------------------
#	Libraries
#------------------------------------------------------------------------------
import os
from shutil import rmtree
from time import time

from utils.map import Map
from utils.search import Astar
from utils.render import render_maps


#------------------------------------------------------------------------------
#   Output directory
#------------------------------------------------------------------------------
OUT_DIR = "outputs/astar/"

if os.path.exists(OUT_DIR):
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

start_time = time()
shortest_path = Astar_obj.search_shortest_path(start=start, stop=stop)
finish_time = time()

print("Number of point:", len(shortest_path))
print("Runtime: %.3f [s]" % (finish_time-start_time))


# Render visualization maps
render_maps(
	Map_obj=Map_obj,
	start=start,
	stop=stop,
	shortest_path=shortest_path,
	out_dir=OUT_DIR,
)