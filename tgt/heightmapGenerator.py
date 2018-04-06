"""
The parent structure that generates heightmaps based
on user preferences.
"""

import random
import noise
import numpy as np
import math
import time

from tgt.preferences import CELL_LENGTH


def init_once(cls, fn):

    return cls(fn())


def analyze_cell(grid, x, y):
    compare = grid[x, y]
    h = grid.shape[0]
    w = grid.shape[1]
    a = x-CELL_LENGTH if x >= CELL_LENGTH else 0
    b = x+CELL_LENGTH if (x+CELL_LENGTH) < w else (w-1)
    c = y-CELL_LENGTH if y >= CELL_LENGTH else 0
    d = y+CELL_LENGTH if (y+CELL_LENGTH) < h else (h-1)
    cell = grid[a:b, c:d]
    total_diff = np.sum(np.abs(cell - compare))
    total_height = np.sum(cell)
    return total_diff, (total_height / (CELL_LENGTH + 1)**2)


def score(grid: np.ndarray) -> tuple:
    start = time.time()
    '''total_in_cell_consistency = 0
    average_heights = []
    num_cells = 0
    h = grid.shape[0]
    w = grid.shape[1]
    for i in range(0, h, CELL_LENGTH*2+1):
        for j in range(0, w, CELL_LENGTH*2+1):
            cell_consistency, cell_average_height = analyze_cell(grid, i, j)
            total_in_cell_consistency += cell_consistency
            average_heights.append(cell_average_height)
            num_cells += 1
    average_cell_consistency = total_in_cell_consistency / num_cells
    cell_height_variance = np.std(np.array(average_heights))
    cell_fitness = (average_cell_consistency - cell_height_variance)'''
    cell_fitness = np.sum(grid)
    #print("Time spent scoring:", time.time()-start)
    return np.array([cell_fitness, ]),


def generate_original_population(h, w, pop_size):
    population = np.array([generate_basic_perlin_noise(h, w) for _ in range(pop_size)])
    return population


def compute_population_fitness(population):
    population_fitness = np.array([score(member) for member in population])
    order = np.argsort(population_fitness)
    return population[order]


def select_from_population(sorted_population, num_from_top, num_from_random):
    next_generation = []
    for i in range(num_from_top):
        next_generation.append(sorted_population[i])
    for i in range(num_from_random):
        next_generation.append(random.choice(sorted_population)[0])
    random.shuffle(next_generation)
    return np.array(next_generation)


def breed(member1: np.ndarray, member2: np.ndarray) -> tuple:
    start = time.time()
    h = member1.shape[0]
    w = member1.shape[1]
    weightings1 = generate_basic_perlin_noise(h, w, octaves=2)
    max_weight = np.max(weightings1)
    min_weight = np.min(weightings1)
    weightings1 = (weightings1 - min_weight) / (max_weight - min_weight)
    member1[...] = (member1.copy() * weightings1) + (member2.copy() * (1-weightings1))

    weightings2 = generate_basic_perlin_noise(h, h, octaves=2)
    max_weight = np.max(weightings2)
    min_weight = np.min(weightings2)
    weightings2 = (weightings2 - min_weight) / (max_weight - min_weight)
    member2[...] = (member1.copy() * weightings2) + (member2.copy() * (1-weightings2))
    # print("Time spent breeding:", time.time()-start)
    return member1, member2


def breed_population(breeders, number_of_children):
    next_population = []
    for i in range(math.ceil(len(breeders)/2)):
        for j in range(number_of_children):
            next_population.append(breed(breeders[i], breeders[len(breeders)-1-i]))
    return np.array(next_population)


def mutate(grid: np.ndarray) -> tuple:
    #start = time.time()
    #h = grid.shape[0]
    #w = grid.shape[1]
    #mutation_value = generate_basic_perlin_noise(h, w, octaves=2)
    #mutation_value = (mutation_value * .05) - .05
    #grid[...] = grid.copy() + mutation_value
    #grid[...] = grid + mutation_value

    mult = np.random.normal(0, np.sqrt(np.std(grid)))
    mult = 100 * int(mult)
    mask = mult * np.random.rand(*grid.shape)
    grid[...] = grid + mask

    # print("Time spent mutating:", time.time()-start)
    return grid,


def mutate_population(population, mutation_chance):
    for i in range(len(population)):
        if random.random() * 100 < mutation_chance:
            population[i] = mutate(population[i])
    return population


def generate_basic_perlin_noise(h, w, octaves=8, persistence=0.5, lacunarity=2.0,
                                repeatx=1024, repeaty=1024, base=0, dtype=np.float32):
    """
    :param h:
    :param w:
    :param octaves:
    :param persistence:
    :param lacunarity:
    :param repeatx:
    :param repeaty:
    :param base:
    :return:
    """
    random.seed(None)
    grid = np.zeros((h,w), dtype=dtype)
    for i in range(h):
        for j in range(w):
            grid[i, j] = noise.pnoise2(i/float(h), j/float(w), octaves, persistence, lacunarity, repeatx, repeaty, base)
    return np.array(grid)


'''def smooth_and_enlarge(grid, new_h, new_w):
    h = grid.shape[0]
    w = grid.shape[1]
    x = np.linspace(0, h, w)
    y = np.linspace(0, h, w)
    f = interpolate.RectBivariateSpline(X, Y, grid)
    newX = np.linspace(0, H, newH)
    newY = np.linspace(0, W, newW)
    biggerGrid = f(newX, newY)
    return biggerGrid'''


def run_genetic_algorithm(h, w, generations=10, population_size=4, num_children=2):
    population = generate_original_population(h, w, population_size)
    num_from_best = math.ceil(population_size/num_children * .75)
    num_from_random = math.floor(population_size/num_children * .25)
    for i in range(generations):
        population = compute_population_fitness(population)
        selection = select_from_population(population, num_from_best, num_from_random)
        children = breed_population(selection, num_children)
        population = mutate_population(children, 0.3)
    return population


def generate(H, W, octaves=1):
    population = run_genetic_algorithm(H, W)
    return population[0]
    # grid = generateBasicPerlinNoise(H, W, octaves)
    # grid = smoothAndEnlarge(grid, H*2, W*2)
    # return grid


def perlin_rand(*args, **kwargs):
    grid = 10000 * generate_basic_perlin_noise(*args,**kwargs)

    mult = np.random.normal(0, 3*np.std(grid))
    mult = 100 * int(mult)
    mask = mult * np.random.rand(*grid.shape)
    return grid + mask
