#------------------------------------------------------------------------------
#   Libraries
#------------------------------------------------------------------------------
import pygame

from grid import GridWorld
from d_star_lite import initDStarLite, moveAndRescan
from utils import stateNameToCoords
from color import *


#------------------------------------------------------------------------------
#   Draw robot
#------------------------------------------------------------------------------
def draw_robot(screen, pos_coords):
	# Draw position
	robot_center = [
		int(pos_coords[0] * (WIDTH + MARGIN) + WIDTH / 2) + MARGIN,
		int(pos_coords[1] * (HEIGHT + MARGIN) + HEIGHT / 2) + MARGIN,
	]
	pygame.draw.circle(screen, RED, robot_center, int(WIDTH / 2) - 2)

	# Draw view range
	vertices = [
		robot_center[0] - VIEWING_RANGE * (WIDTH + MARGIN),
		robot_center[1] - VIEWING_RANGE * (HEIGHT + MARGIN),
		2 * VIEWING_RANGE * (WIDTH + MARGIN),
		2 * VIEWING_RANGE * (HEIGHT + MARGIN),
	]
	pygame.draw.rect(screen, BLUE, vertices, 2)


#------------------------------------------------------------------------------
#   Draw goal cell
#------------------------------------------------------------------------------
def draw_goal_cell(screen, goal_coords):
	vertices = [
		(MARGIN + WIDTH) * goal_coords[0] + MARGIN,
		(MARGIN + HEIGHT) * goal_coords[1] + MARGIN,
		WIDTH, HEIGHT,
	]
	pygame.draw.rect(screen, GREEN, vertices)


#------------------------------------------------------------------------------
#   Draw grid
#------------------------------------------------------------------------------
def draw_grid(screen, graph, basicfont):
	for row in range(Y_DIM):
		for column in range(X_DIM):
			vertices = [
				(MARGIN + WIDTH) * column + MARGIN,
				(MARGIN + HEIGHT) * row + MARGIN,
				WIDTH, HEIGHT,
			]
			pygame.draw.rect(screen, colors[graph.cells[row][column]], vertices)

			node_name = 'x' + str(column) + 'y' + str(row)
			if(graph.graph[node_name].g != float('inf')):
				text = basicfont.render(str(graph.graph[node_name].g), True, (0, 0, 200))
				textrect = text.get_rect()
				textrect.centerx = int(column * (WIDTH + MARGIN) + WIDTH / 2) + MARGIN
				textrect.centery = int(row * (HEIGHT + MARGIN) + HEIGHT / 2) + MARGIN
				screen.blit(text, textrect)


#------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------
# Set the HEIGHT and WIDTH of the screen
X_DIM = Y_DIM = 15
MARGIN = 5
WIDTH = HEIGHT = 50
VIEWING_RANGE = 5

WINDOW_SIZE = [
	(WIDTH + MARGIN) * X_DIM + MARGIN,
	(HEIGHT + MARGIN) * Y_DIM + MARGIN,
]

# Node names
s_start = 'x1y2'
s_goal = 'x5y4'
goal_coords = stateNameToCoords(s_goal)


#------------------------------------------------------------------------------
#   Setup
#------------------------------------------------------------------------------
# Create GUI
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("D* Lite Path Planning")
clock = pygame.time.Clock()
basicfont = pygame.font.SysFont('Comic Sans MS', 36)

# Create grid
graph = GridWorld(X_DIM, Y_DIM, connect8=False)
graph.setStart(s_start)
graph.setGoal(s_goal)

# Initialize D* Lite
k_m = 0
queue = []

graph, queue, k_m = initDStarLite(graph, queue, s_start, s_goal, k_m)

s_current = s_start
pos_coords = stateNameToCoords(s_current)


#------------------------------------------------------------------------------
#   Main loop
#------------------------------------------------------------------------------
done = False

while not done:
	# Check events from user
	for event in pygame.event.get(): 
		# Exit program
		if event.type==pygame.QUIT:  
			done = True

		# Move robot
		elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
			s_new, k_m = moveAndRescan(graph, queue, s_current, VIEWING_RANGE, k_m)

			if s_new == 'goal':
				print('Goal Reached!')
				done = True

			else:
				s_current = s_new
				pos_coords = stateNameToCoords(s_current)

		# Set obstacle
		elif event.type==pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			graph.cells[row][column] = -1 if(graph.cells[row][column]==0) else 0


	# Draw and update frame
	screen.fill(BLACK)
	draw_grid(screen, graph, basicfont)
	draw_goal_cell(screen, goal_coords)
	draw_robot(screen, pos_coords)

	clock.tick(20)
	pygame.display.flip()


# Quit procedure
pygame.quit()