import pytest

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


@pytest.mark.parametrize('sx', [-1, 1])
@pytest.mark.parametrize('sy', [-1, 1])
@pytest.mark.parametrize('swap_axes', [False, True])
def test_raytrace_all_octants(sx, sy, swap_axes):
    # Reflect a known line about its starting cell, then swap the axes.
    expected = [
        [0, 0], [0, 1], [1, 1], [1, 2], [1, 3], [1, 4], [2, 4], [2, 5]
    ]
    expected = [[sx * x, sy * y] for x, y in expected]
    if swap_axes:
        expected = [[y, x] for x, y in expected]
    expected = [[x + 5, y + 5] for x, y in expected]

    assert raytrace(expected[0], expected[-1]) == expected


@pytest.mark.parametrize('end, expected', [
    ([1, 3], [[3, 3], [2, 3], [1, 3]]),
    ([5, 3], [[3, 3], [4, 3], [5, 3]]),
    ([3, 1], [[3, 3], [3, 2], [3, 1]]),
    ([3, 5], [[3, 3], [3, 4], [3, 5]]),
    ([3, 3], [[3, 3]]),
])
def test_raytrace_axis_aligned_and_stationary(end, expected):
    assert raytrace([3, 3], end) == expected


@pytest.mark.parametrize('use_raytrace', [False, True])
def test_smoothen_path(use_raytrace):
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
    # The grid is empty, so the intermediate waypoints are unnecessary.
    assert smoothen_path(grid, path, use_raytrace=use_raytrace) == [
        [0, 0], [4, 4]
    ]
