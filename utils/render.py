#------------------------------------------------------------------------------
#	Libraries
#------------------------------------------------------------------------------
from multiprocessing import Pool, cpu_count
from itertools import repeat
from tqdm import tqdm
import os


#------------------------------------------------------------------------------
#	Pool function for rendering a visualization map
#------------------------------------------------------------------------------
def pool_render_map(args):
	Map_obj, start, stop, idx, path, out_dir = args
	Map_obj.visualize_map(
		start=start,
		stop=stop,
		path=path, 
		savename=os.path.join(out_dir, "%d.png" % (idx)),
	)


#------------------------------------------------------------------------------
#	Render visualization maps
#------------------------------------------------------------------------------
def render_maps(Map_obj, start, stop, shortest_path, out_dir):
	n_points = len(shortest_path)
	paths, path = [], []
	for point in shortest_path:
		path.append(point)
		paths.append(path.copy())

	pools = Pool(processes=cpu_count())
	args = zip(repeat(Map_obj), repeat(start), repeat(stop), range(n_points), paths, repeat(out_dir))

	print("Render visualization maps...")
	for _ in tqdm(pools.imap_unordered(pool_render_map, args), total=n_points):
		pass