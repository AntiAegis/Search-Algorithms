#------------------------------------------------------------------------------
#	Libraries
#------------------------------------------------------------------------------
import numpy as np 
from matplotlib import pyplot as plt


#------------------------------------------------------------------------------
#	Map object
#------------------------------------------------------------------------------
class Map(object):
	def __init__(self, height, width, barrier,
		background_val=0, barrier_val=1, start_val=2, stop_val=3, path_val=4):
		super(Map, self).__init__()
		self.height = height
		self.width = width
		self.barrier = barrier
		self.background_val = background_val
		self.barrier_val = barrier_val
		self.start_val = start_val
		self.stop_val = stop_val
		self.path_val = path_val

		# Create matrix of map
		self.map = np.ones([height, width]) * background_val
		x = [b[0] for b in barrier]
		y = [b[1] for b in barrier]
		self.map[y, x] = barrier_val


	def visualize_map(self, start=None, stop=None, path=None, fig_idx=1, block=True, savename=False):
		fig = plt.figure(fig_idx)
		plt.clf()
		ax = fig.add_subplot(1, 1, 1)
		width_ticks = np.arange(0.5, self.width+0.5)
		ax.set_xticks(width_ticks)
		ax.set_xticklabels([])
		height_ticks = np.arange(0.5, self.height+0.5)
		ax.set_yticks(height_ticks)
		ax.set_yticklabels([])
		map_ = self.map.copy()

		# Add path
		if path is not None:
			for x, y in path:
				map_[y, x] = self.path_val

		# Add start and stop points
		if (start is not None) and (stop is not None):
			map_[start[1], start[0]] = self.start_val
			map_[stop[1], stop[0]] = self.stop_val

		# Convert to RGB image
		map_rgb = np.zeros([map_.shape[0], map_.shape[1], 3], np.uint8)

		map_rgb[map_==self.background_val, 0] = 255
		map_rgb[map_==self.background_val, 1] = 255
		map_rgb[map_==self.background_val, 2] = 255

		map_rgb[map_==self.barrier_val, 0] = 0
		map_rgb[map_==self.barrier_val, 1] = 0
		map_rgb[map_==self.barrier_val, 2] = 0

		map_rgb[map_==self.path_val, 0] = 255
		map_rgb[map_==self.path_val, 1] = 255
		map_rgb[map_==self.path_val, 2] = 0

		map_rgb[map_==self.start_val, 0] = 0
		map_rgb[map_==self.start_val, 1] = 255
		map_rgb[map_==self.start_val, 2] = 0

		map_rgb[map_==self.stop_val, 0] = 255
		map_rgb[map_==self.stop_val, 1] = 0
		map_rgb[map_==self.stop_val, 2] = 0

		# Show the map
		plt.imshow(map_rgb)
		plt.grid(True, which='major', color='b', linestyle='-', linewidth=1)
		if savename:
			plt.savefig("%s.png" % (savename))
		else:
			plt.show(block=block)


#------------------------------------------------------------------------------
#	Test bench
#------------------------------------------------------------------------------
# # Create an instance of map
# barrier = [
# 	(15,15), (15,14), (15,13), (15,12), (15,11), (15,10), (15,9), (15,8),
# 	(15,15), (14,15), (13,15), (12,15), (11,15), (10,15), (9,15), (8,15),

# 	(14,15), (14,14), (14,13), (14,12), (14,11), (14,10), (14,9), (14,8),
# 	(15,14), (14,14), (13,14), (12,14), (11,14), (10,14), (9,14), (8,14),
# ]
# map_obj = Map(height=25, width=25, barrier=barrier)


# # Define starting and stop points
# start = (0,0)
# stop = (24,24)


# # Visualize map
# map_obj.visualize_map(start=start, stop=stop)