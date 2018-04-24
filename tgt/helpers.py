"""
The parent structure that generates heightmaps based
on user preferences.
"""

import numpy as np
import random
import noise
import math
import time
from tgt.preferences import CELL_LENGTH


def init_once(cls, fn):
    """
    :param cls: a class to instantiate
    :param fn: a function of no arguments to call and pass to cls
    :return: cls(fn())
    """

    return cls(fn())


def crossover(par1: np.ndarray, par2: np.ndarray) -> tuple:
    """
    :param par1: one parent
    :param par2: the other parent
    :return: children of the parents
    """

    tmp1 = par1.copy()
    tmp2 = par2.copy()
    par1[...] = tmp1 + tmp2
    par2[...] = tmp1 - tmp2
    return par2, par2


def mutate(individual: np.ndarray) -> tuple:
    """
    :param individual: candidate to mutate
    :return: mutated individual
    """

    mult = np.random.normal(0, np.sqrt(np.std(individual)))
    mult = 20 * int(mult)
    mask = mult * np.random.rand(*individual.shape)

    individual[...] = individual + mask
    return individual,


def score(individual: np.ndarray) -> tuple:
    """
    :param individual: candidate to score
    :return: tuple of scores for the individual
    """

    metrics = [loc_glbl_var, sea_level, bedrock, mountains]
    result = tuple(metric(individual) for metric in metrics)
    return result


def loc_glbl_var(individual: np.ndarray) -> float:
    """
    Computes score as function of quadrant and global variance
    :param individual: candidate to score
    :return: sum of quadrant variance - 5*global variance
    """

    mids = tuple(map(lambda x: int(x/2), individual.shape))
    s1 = np.var(individual[:mids[0], :mids[1]])
    s2 = np.var(individual[:mids[0], mids[1]:])
    s3 = np.var(individual[mids[0]:, :mids[1]])
    s4 = np.var(individual[mids[0]:, mids[1]:])
    result = s1 + s2 + s3 + s4 - 10*np.var(individual[...])
    return float(result)


def sea_level(individual: np.ndarray, target: float = 25.0) ->float:
    """
    :param individual: candidate to score
    :param target: ideal sea level height
    :return: |individual - target|_2
    """

    return np.linalg.norm(individual - target)


def bedrock(individual: np.ndarray, target: float = -2000.0) -> float:
    """
    :param individual: candidate to score
    :param target: ideal bedrock height
    :return: |min(individual) - target|_2
    """

    return np.linalg.norm(np.min(individual) - target)


def mountains(individual: np.ndarray, target: float = 3500.0) -> float:
    """
    :param individual: candidate to score
    :param target: ideal mountains heights
    :return: |max(individual) - target|_2
    """

    return np.linalg.norm(np.max(individual) - target)


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


def crossover2(member1: np.ndarray, member2: np.ndarray) -> tuple:
    h = member1.shape[0]
    w = member1.shape[1]

    weightings1 = np.random.rand(h, w)
    max_weight = np.max(weightings1)
    min_weight = np.min(weightings1)
    weightings1 = (weightings1 - min_weight) / \
                  (max_weight - min_weight)
    member1[...] = (member1.copy() * weightings1) + \
                   (member2.copy() * (1-weightings1))

    weightings2 = np.random.rand(h, w)
    max_weight = np.max(weightings2)
    min_weight = np.min(weightings2)
    weightings2 = (weightings2 - min_weight) / \
                  (max_weight - min_weight)
    member2[...] = (member1.copy() * weightings2) + \
                   (member2.copy() * (1-weightings2))

    return member1, member2


def mutate2(grid: np.ndarray) -> tuple:
    """
    :param grid: heightmap to mutate
    :return: mutated heightmap
    """

    mult = np.random.normal(0, np.sqrt(np.std(grid)))
    mult = 100 * int(mult)
    mask = mult * np.random.rand(*grid.shape)
    grid[...] = grid + mask

    return grid,


def generate_basic_perlin_noise(h, w, octaves=8,
                                persistence=0.5, lacunarity=2.0,
                                repeatx=1024, repeaty=1024, base=0,
                                dtype=np.float32):
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
    grid = np.zeros((h, w), dtype=dtype)
    for i in range(h):
        for j in range(w):
            grid[i, j] = noise.pnoise2(i/float(h), j/float(w),
                                       octaves, persistence,
                                       lacunarity, repeatx,
                                       repeaty, base)
    return np.array(grid)


def perlin_rand(*args, **kwargs):
    grid = 100 * generate_basic_perlin_noise(*args, **kwargs)

    mult = np.random.normal(0, 3*np.std(grid))
    mult = 100 * int(mult)
    mask = mult * np.random.rand(*grid.shape)
    return grid + mask
