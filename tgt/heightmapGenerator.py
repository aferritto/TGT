'''
The parent structure that generates heightmaps based
on user preferences.
'''

import random
import noise
import numpy as np

'''
This will call the currently best heightmap generator algorithm.
'''
def generate(H, W, octaves=1):
    return generateBasicPerlinNoise(H, W, octaves)

'''
A basic generator that makes perlin noise
'''
def generateBasicPerlinNoise(H, W, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0):
    random.seed(None)
    grid = np.zeros((H,W))
    for i in range(H):
        for j in range(W):
            grid[i, j] = noise.pnoise2(i/float(H), j/float(W), octaves, persistence, lacunarity, repeatx, repeaty, base)
    return grid