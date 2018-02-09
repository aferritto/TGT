import pytest
from tgt import heightmapGenerator
import numbers

H = 700
W = 400

def test_generate():
    grid = heightmapGenerator.generate(H, W)
    assert len(grid) == H
    assert len(grid[0]) == W
    for row in grid:
        for num in row:
            assert isinstance(num, numbers.Number)

def test_generateRandomPerlinNoise():
    grid = heightmapGenerator.generateBasicPerlinNoise(H, W)
    assert len(grid) == H
    assert len(grid[0]) == W
    for row in grid:
        for num in row:
            assert isinstance(num, numbers.Number)