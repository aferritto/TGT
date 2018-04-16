"""
Tests visualizer. The best way to test main is the run it, however.
"""
import pytest
from tgt import visualizer as vis

grid = [[0, 0, 0],
        [0, .5, 0],
        [.5, .25, 0]]


def test_plot2D():
    vis.plot2D(grid, False)


def test_plot3D():
    vis.plot3D(grid, False)
