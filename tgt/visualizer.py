'''
This program will visualize a terrain given by a heightmap in a CSV file using Matplotlib.
It generates two views: a 2D heightmap and a 3D terrain structure.
As an argument, it should be given the heightmap CSV
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

'''
Plot a 2D heatmap of the data.
@param grid a 2 dimensional array to plot
'''
def plot2D(grid):
    plt.imshow(grid, cmap='hot', interpolation='nearest')
    plt.show()

'''
Plot a 3D heatmap of the data.
@param grid a 2 dimensional array to plot
'''
def plot3D(grid):
    X, Y = np.meshgrid(np.arange(0,len(grid)), np.arange(0,len(grid[0])))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, grid, cmap=cm.coolwarm)
    ax.set_zlim(-.5, .5)
    plt.show()

'''
Plot data based on a CSV argument
@arg the filename of a CSV containing the heightmap data
'''
def main():
    heightmapFile = sys.argv[1]
    heightmap = []
    with open(heightmapFile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            heightmap.append(row)
    plot2D(heightmap)
    plot3D(heightmap)

if __name__ == '__main__': main()