'''
The parent structure that generates heightmaps based
on user preferences.
'''

import random
import noise
import numpy as np
from scipy import interpolate
import math

CELL_LENGTH = 4

def analyzeCell(grid, x, y):
    totalDiff = 0
    totalHeight = 0
    compare = grid[x, y]
    for i in range(x - CELL_LENGTH, x + CELL_LENGTH):
        for j in range(y - CELL_LENGTH, y + CELL_LENGTH):
            if(i > 0 and i < grid.shape[0] and j > 0 and j < grid.shape[1]):
                totalDiff += abs(compare - grid[i, j])
                totalHeight += grid[i, j]
    return totalDiff, (totalHeight / (CELL_LENGTH + 1)**2)

def fitness(grid):
    totalInCellConsistency = 0
    averageHeights = []
    numCells = 0
    H = grid.shape[0]
    W = grid.shape[1]
    for i in range(H):
        for j in range(W):
            cellConsistency, cellAverageHeight = analyzeCell(grid, i, j)
            totalInCellConsistency += cellConsistency
            averageHeights.append(cellAverageHeight)
            numCells += 1
    averageCellConsistency = totalInCellConsistency / numCells
    cellHeightVariance = np.std(np.array(averageHeights))
    fitness = (averageCellConsistency - cellHeightVariance)
    return fitness

def generateOriginalPopulation(H, W, popSize):
    population = np.array([generateBasicPerlinNoise(H, W) for _ in range(popSize)])
    return population

def computePopulationFitness(population):
    populationFitness = np.array([fitness(member) for member in population])
    order = np.argsort(populationFitness)
    return population[order]

def selectFromPopulation(sortedPopulation, numFromTop, numFromRandom):
    nextGeneration = []
    for i in range(numFromTop):
        nextGeneration.append(sortedPopulation[i])
    for i in range(numFromRandom):
        nextGeneration.append(random.choice(sortedPopulation)[0])
    random.shuffle(nextGeneration)
    print(numFromTop)
    print(numFromRandom)
    return np.array(nextGeneration)

def breed(member1, member2):
    H = member1.shape[0]
    W = member1.shape[1]
    weightings = generateBasicPerlinNoise(H, W, octaves = 2)
    max = np.max(weightings)
    min = np.min(weightings)
    weightings = (weightings - min) / (max - min)
    child = (member1 * weightings) + (member2 * (1-weightings))
    return child

def breedPopulation(breeders, numberOfChildren):
    nextPopulation = []
    for i in range(math.ceil(len(breeders)/2)):
        for j in range(numberOfChildren):
            nextPopulation.append(breed(breeders[i], breeders[len(breeders)-1-i]))
    return np.array(nextPopulation)

def mutate(grid):
    H = grid.shape[0]
    W = grid.shape[1]
    mutationValue = generateBasicPerlinNoise(H, W, octaves=4)
    mutationValue = (mutationValue * .1) - .05
    grid += mutationValue
    return grid

def mutatePopulation(population, mutationChance):
    for i in range(len(population)):
        if random.random() * 100 < mutationChance:
            population[i] = mutate(population[i])
    return population

def generateBasicPerlinNoise(H, W, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0):
    ''' A basic generator that makes perlin noise '''
    random.seed(None)
    grid = np.zeros((H,W))
    for i in range(H):
        for j in range(W):
            grid[i, j] = noise.pnoise2(i/float(H), j/float(W), octaves, persistence, lacunarity, repeatx, repeaty, base)
    return np.array(grid)

def smoothAndEnlarge(grid, newH, newW):
    H = grid.shape[0]
    W = grid.shape[1]
    X = np.linspace(0, H, W)
    Y = np.linspace(0, H, W)
    f = interpolate.RectBivariateSpline(X, Y, grid)
    newX = np.linspace(0, H, newH)
    newY = np.linspace(0, W, newW)
    biggerGrid = f(newX, newY)
    return biggerGrid

def runGeneticAlgorithm(H, W, generations=10, populationSize=4, numChildren=2):
    population = generateOriginalPopulation(H, W, populationSize)
    numFromBest = math.ceil(populationSize/numChildren * .75)
    numFromRandom = math.floor(populationSize/numChildren * .25)
    for i in range(generations):
        population = computePopulationFitness(population)
        print(population.shape)
        selection = selectFromPopulation(population, numFromBest, numFromRandom)
        print(selection.shape)
        children = breedPopulation(selection, numChildren)
        print(children.shape)
        population = mutatePopulation(children, 0.3)
        print(population.shape)
    return population

def generate(H, W, octaves=1):
    ''' This will call the currently best heightmap generator algorithm. '''
    population = runGeneticAlgorithm(H, W)
    return population[0]
    #grid = generateBasicPerlinNoise(H, W, octaves)
    #grid = smoothAndEnlarge(grid, H*2, W*2)
    #return grid
