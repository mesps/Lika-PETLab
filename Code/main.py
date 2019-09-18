import sys
import os
import random
import math
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pygame
from pygame.locals import *

# Colors to be used on pygame
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (204, 0, 0)
grey = (210, 210, 210)
blue =  (61, 133, 198)
yellow = (255, 255, 0)

# Initializing pygame
pygame.init()

# Name to be displayed on pygame
pygame.display.set_caption("Robot Map")

# Possible states for each cell
livre = 0
visitado = 1
robo = 2
obstaculo = 3
alcool_temp = 7 
# alcool_temp is a temporary variable to show where the alcohol would be on the map

# Matrix size, the bigger the matrix, the slower the program will run
os.system('clear')
max_size = int(input('Digite a dimensão N do mapa quadrado NxN:\n'))

# Margin between blocks on pygame
margin = 1

# Setting block's sizes for pygame
width = (350 - margin)/max_size - margin
height = (350 - margin)/max_size - margin

# Setting the screen size for pygame
screen_width = 350
screen_height = 350
WINDOW_SIZE = [350, 350]

# Setting screen mode for pygame
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Knowing the time to update frame
clock = pygame.time.Clock()
frame = max_size*100

# Map
matrix = []
alcoolmap = [[0]*max_size for i in range (0, max_size)]

# Robot's movimentation matrix with priorities
moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]

# Robot's path
path = [[] for i in range(0, 4)]

# Initializing matrix
def matrix_init():
	for i in range (0, max_size):
		line = []
		for j in range (0, max_size):
			num = random.random()
			# Generating map randomly
			if num <= 0.1:
				new_cell = alcool_temp
			elif num > 0.1 and num <= 0.2:
				new_cell = obstaculo
			else:
				new_cell = livre
			line.append(new_cell)
		matrix.append(line)

	

# Showing matrix on termianl
def print_matrix():
	for i in range (0, max_size):
		for j in range (0, max_size):
			if matrix[i][j] == robo:
				CRED = '\033[91m'
				CEND = '\033[0m'
			elif matrix[i][j] == visitado:
				CRED = '\033[34m'
				CEND = '\033[0m'
			elif matrix[i][j] == obstaculo:
				CRED = '\033[92m'
				CEND = '\033[0m'
			elif matrix[i][j] == alcool_temp:
				CRED = '\033[33m'
				CEND = '\033[0m'
			else:
				CRED = '\033[0m'
				CEND = '\033[0m'
			print(CRED + str(matrix[i][j]) + CEND, sep="", end=" ")
		print("\n")

# Verifying if there's free cells 
def verify_matrix():
	for i in range (0, max_size):
		for j in range (0, max_size):
			if matrix[i][j] == livre or matrix[i][j] == alcool_temp:
				return True
	return False


# Verify if the coordinate is on the matrix's limit
def verify_coord(newi, newj):
	return newi >= 0 and newi < max_size and newj >= 0 and newj < max_size 

def cross(coords, i):
		if coords[i][1]+1 < max_size:
			# Looking all the cells on the robot's right side
			for j in range (coords[i][1]+1, max_size):
				if matrix[coords[i][0]][j] == obstaculo or matrix[coords[i][0]][j] == robo:
					# If there's a robot or obstacle on the robot's right side then it can't move
					# So stop analysis
					break
				elif matrix[coords[i][0]][j] == livre or matrix[coords[i][0]][j] == alcool_temp:
					# If the robot didn't found a robot or obstable on its right side and there's a free cell
					# Then it will return the right cell_ _ _ _ _ _      
					newj = coords[i][1] + 1              #         |
					if verify_coord(coords[i][0], newj): #         |
						return (0, 1) # <---------------------------
				else: continue
		if coords[i][1]-1 >= 0:
			# Same analysis for the left side
			for j in range (coords[i][1]-1, -1, -1):
				if matrix[coords[i][0]][j] == obstaculo or matrix[coords[i][0]][j] == robo:
					break
				elif matrix[coords[i][0]][j] == livre or matrix[coords[i][0]][j] == alcool_temp:
					newj = coords[i][1] - 1
					if verify_coord(coords[i][0], newj):
						return (0, -1)
				else: continue
		if coords[i][0]+1 < max_size:
			# Same analysis for the down side
			for j in range (coords[i][0]+1, max_size):
				if matrix[j][coords[i][1]] == obstaculo or matrix[j][coords[i][1]] == robo:
					break
				elif matrix[j][coords[i][1]] == livre or matrix[j][coords[i][1]] == alcool_temp:
					newi = coords[i][0] + 1
					if verify_coord(newi, coords[i][1]):
						return (1, 0)
				else: continue
		if coords[i][0]-1 >= 0:
			# Same analysis for the up side
			for j in range (coords[i][0]-1, -1, -1):
				if matrix[j][coords[i][1]] == obstaculo or matrix[j][coords[i][1]] == robo:
					break
				elif matrix[j][coords[i][1]] == livre or matrix[j][coords[i][1]] == alcool_temp:
					newi = coords[i][0] - 1
					if verify_coord(newi, coords[i][1]):
						return (-1, 0)
				else: continue
		
		# If there's no free cell on this analysis, the robot wont move 
		return (0, 0)


# Updateing matrix
def change_matrix(coords):
	# Analyzing each robot
	for i in range (0, 4):
		flag = 0 # If the robot moved: flag = 1, else flag = 0
		# Analyzing each robot's moviment
		for j in range (0, 4):
			# Calculating new coordinates
			newi = coords[i][0] + moves[j][0]
			newj = coords[i][1] + moves[j][1]
			if verify_coord(newi, newj):
				# If there's alcohol on the cell, save it on the alcohol map
				if matrix[newi][newj] == alcool_temp:
						alcoolmap[newi][newj] = alcool_temp
				# If the cell is free, the robot will move to it
				if matrix[newi][newj] == livre or matrix[newi][newj] == alcool_temp:
					matrix[newi][newj] = (robo)
					matrix[coords[i][0]][coords[i][1]] = (visitado)
					# Ativando a flag
					flag = 1
					path[i].append((coords[i][0], coords[i][1]))
					coords[i][0] = newi
					coords[i][1] = newj
					break #If this robot moved, then stop the current analysis

		# If the robot didn't move, it will look for free cell in a cross
		if not flag:
			# Get the movimentation that will be done by the robot (after cross analysis)
			(movi, movj) = cross(coords, i)
			
			# If (movi, movj) = (0,0) it means that there's no free cell on the cross
			if (movi, movj) != (0, 0):
				# Move robot
				matrix[coords[i][0]][coords[i][1]] = (visitado)
				path[i].append((coords[i][0], coords[i][1]))
				flag = 1
				coords[i][0] = coords[i][0] + movi
				coords[i][1] = coords[i][1] + movj
				matrix[coords[i][0]][coords[i][1]] = (robo)

		# If the robot didn't move, it will go back one cell back on its path, and analyse again
		if not flag and path[i]:
			flag = 0
			newcoord = path[i].pop()
			matrix[newcoord[0]][newcoord[1]] = (robo)
			matrix[coords[i][0]][coords[i][1]] = (visitado)
			coords[i][0] = newcoord[0]
			coords[i][1] = newcoord[1]

# Spreading alcohol on the heatmap matrix
def heatmap():
	for i in range (0, max_size):
		for j in range (0, max_size):
			if alcoolmap[i][j] == alcool_temp:
				alcoolmap[i][j] = 100
				if i - 1 > 0: alcoolmap[i-1][j] = 95
				if i + 1 < max_size: alcoolmap[i+1][j] = 90
				if j - 1 > 0: alcoolmap[i][j-1] = 85
				if j + 1 < max_size: alcoolmap[i][j+1] = 90

# Plotting heatmap
def print_heatmap(map):
	plt.imshow(alcoolmap, interpolation='sinc', cmap='rainbow')

	# Saving heatmap as png
	if map: plt.savefig('heatmap1.png')
	if not map: plt.savefig('heatmap2.png')

	# Showing heatmap
	plt.show()

def color_map():
	for i in range (max_size):
		for j in range (max_size):
			# Setting the color of the block
			if matrix[i][j] == robo:
				color = red
			elif matrix[i][j] == visitado:
				color = blue
			elif matrix[i][j] == obstaculo:
				color = green
			elif matrix[i][j] == alcool_temp:
				color = yellow
			else:
				color = grey
			
			# Updating the block's color
			pygame.draw.rect(screen,
							color,
							[(margin + width) * j + margin,
							(margin + height) * i + margin,
							width,
							height])

			# Frames per second
			clock.tick(frame)

			# Updating the screen
			pygame.display.flip()

def main():
	# Coordinates where the robots will start
	coords = [[max_size-1, max_size//2 - 1], [max_size-1, max_size//2], [max_size-1, max_size//2 + 1], [max_size-1, max_size//2 + 2]]
	matrix_init()

	# Positionating the robots on the map
	for i in range (0, 4):
		matrix[coords[i][0]][coords[i][1]] = (robo)

	passos = 0	#How many steps it took to finish the map matrix

	# Setting the screen background
	screen.fill(white)

	print_matrix()
	while verify_matrix() == True:
		os.system('clear')

		# Calling func which updates the map matrix
		change_matrix(coords) 
		
		# Counting how many steps it took to cover the whole map
		passos+=1

		# Visualize map on terminal
		print_matrix()

		# Visualize map with pygame
		color_map()

		time.sleep(0.1)

	print(passos)
	
	# Heatmap that the alcohol isn't spread out
	print_heatmap(1)

	# Heatmap that the alcohol is spread out (more realistic)
	heatmap()
	print_heatmap(0)

	# Wait to close the pygame simulation
	time.sleep(0.5)
	pygame.quit()

	return 0


main()