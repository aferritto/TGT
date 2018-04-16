import pytest
from tgt import heightmapGenerator
import numbers

H = 700
W = 400


def test_generate_random_perlin_noise():
    grid = heightmapGenerator.generate_basic_perlin_noise(H, W)
    assert len(grid) == H
    assert len(grid[0]) == W
    for row in grid:
        for num in row:
            assert isinstance(num, numbers.Number)
