from pathfinding.core.grid import Grid
from pathfinding.core.util import bresenham, raytrace, smoothen_path


def test_bresenham():
    """
    test bresenham path interpolation
    """
    assert bresenham([0, 0], [2, 5]) == [
        [0, 0], [0, 1],
        [1, 2], [1, 3],
        [2, 4], [2, 5]
    ]
    assert bresenham([0, 1], [0, 4]) == [
        [0, 1], [0, 2], [0, 3], [0, 4]
    ]


def test_raytrace():
    """
    test raytrace path interpolation
    """
    assert raytrace([0, 0], [2, 5]) == [
        [0, 0], [0, 1],
        [1, 1], [1, 2], [1, 3], [1, 4],
        [2, 4], [2, 5]
    ]
    assert raytrace([0, 1], [0, 4]) == [
        [0, 1], [0, 2], [0, 3], [0, 4]
    ]


def test_smoothen_path():
    matrix = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    grid = Grid(matrix=matrix)
    path = [
        [0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [3, 3], [3, 4], [4, 4]
    ]
    smooth_path = [
        [0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [3, 3], [4, 4]
    ]
    assert smoothen_path(grid, path) == smooth_path
