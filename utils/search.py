#------------------------------------------------------------------------------
#	Libraries
#------------------------------------------------------------------------------
import numpy as np
from collections import defaultdict


#------------------------------------------------------------------------------
#	Euclidean distance
#------------------------------------------------------------------------------
def euclidean_dist(p1, p2):
	dx = p1[0] - p2[0]
	dy = p1[1] - p2[1]
	dist = np.sqrt(dx**2 + dy**2)
	return dist


#------------------------------------------------------------------------------
#	Search algorithm using A*
#------------------------------------------------------------------------------
class Astar(object):
	def __init__(self, map_matrix, lamda={"g": 1.0, "h": 1.0}):
		super(Astar, self).__init__()
		self.map = map_matrix.copy()
		self.lamda = lamda


	def search_shortest_path(self, start, stop):
		# The set of nodes already evaluated
		closedSet = []

		# The set of currently discovered nodes that are not evaluated yet
		openSet = [start]

		# For each node, which node it can most efficiently be reached from.
		# If a node can be reached from many nodes, cameFrom will eventually contain the
		# most efficient previous step.
		# cameFrom = defaultdict(lambda: [])
		cameFrom = {}

		# For each node, the cost of getting from the start node to that node.
		gScore = defaultdict(lambda: np.inf)
		gScore[self.to_index(start)] = 0

		# For each node, the total cost of getting from the start node to the goal
		# by passing by that node. That value is partly known, partly heuristic.
		fScore = defaultdict(lambda: np.inf)
		fScore[self.to_index(start)] = self.heuristic_cost_estimate(start, stop)

		# Loop until reach the stop point
		while len(openSet):
			# current is the node in openSet having the lowest fScore value
			lowest_fScore_val = np.inf
			for node in openSet:
				fScore_val = fScore[self.to_index(node)]
				if fScore_val < lowest_fScore_val:
					lowest_fScore_val = fScore_val
					current = node
			if current==stop:
				total_path = self.reconstruct_path(cameFrom, current)
				return total_path

			openSet.remove(current)
			closedSet.append(current)

			# Loop over neighbors of current
			neighbors = self.get_neighbors(current)
			for neighbor in neighbors:
				# Ignore the neighbor which is already evaluated
				if neighbor in closedSet:
					continue

				# The distance from start to a neighbor
				g_cost = gScore[self.to_index(current)]
				h_cost = self.dist_between(current, neighbor)
				tentative_gScore = self.lamda['g']*g_cost + self.lamda['h']*h_cost

				# Discover a new node
				if neighbor not in openSet:
					openSet.append(neighbor)
				# This is not a better path
				elif tentative_gScore >= gScore[self.to_index(neighbor)]:
					continue

				# This path is the best until now. Record it!
				cameFrom[self.to_index(neighbor)] = current
				gScore[self.to_index(neighbor)] = tentative_gScore

				g_cost = gScore[self.to_index(neighbor)]
				h_cost = self.heuristic_cost_estimate(neighbor, stop)
				fScore[self.to_index(neighbor)] = self.lamda['g']*g_cost + self.lamda['h']*h_cost


	def heuristic_cost_estimate(self, point1, point2):
		return euclidean_dist(point1, point2)


	def dist_between(self, point1, point2):
		return 1.0


	def to_index(self, point):
		x, y = point
		return y * self.map.shape[1] + x


	def index_to(self, idx):
		y = idx // self.map.shape[1]
		x = idx - y * self.map.shape[1]
		return x, y


	def get_neighbors(self, point):
		x, y = point
		up, bottom, left, right = (x,y-1), (x,y+1), (x-1,y), (x+1,y)
		neighbors = []
		for x, y in [up, bottom, left, right]:
			if ((x>=0) and
				(y>=0) and
				(x<self.map.shape[1]) and
				(y<self.map.shape[0]) and
				(self.map[y,x]==0)
			):
				neighbors.append((x, y))

		return neighbors


	def reconstruct_path(self, cameFrom, current):
		total_path_temp = []
		for point in cameFrom.keys():
			point = cameFrom[point]
			total_path_temp.append(point)
		total_path_temp.append(current)

		total_path = []
		for point in total_path_temp:
			if point not in total_path:
				total_path.append(point)
		return total_path


#------------------------------------------------------------------------------
#	Search algorithm using Dijkstra
#------------------------------------------------------------------------------
class Dijkstra(Astar):
	"""
	Dijkstra is a special case of A* with weigth_cost = {"g": 1.0, "h": 0.0}
	"""
	def __init__(self, map_matrix):
		Astar.__init__(
			self, 
			map_matrix=map_matrix.copy(),
			lamda={"g": 1.0, "h": 0.0},
		)