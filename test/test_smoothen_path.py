import pytest

from pathfinding.core.grid import Grid
from pathfinding.core.util import smoothen_path


@pytest.mark.parametrize('use_raytrace', [False, True])
@pytest.mark.parametrize('reverse', [False, True])
def test_smoothen_path_checks_shortcut_to_destination(use_raytrace, reverse):
    grid = Grid(matrix=[[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    path = [[0, 0], [0, 2], [2, 2]]
    if reverse:
        path.reverse()

    # Removing the bend would send the path through the center obstacle.
    assert smoothen_path(grid, path, use_raytrace=use_raytrace) == path


@pytest.mark.parametrize('use_raytrace', [False, True])
def test_smoothen_path_keeps_last_visible_waypoint(use_raytrace):
    grid = Grid(matrix=[
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ])
    path = [[0, 0], [0, 2], [0, 4], [4, 4], [4, 0]]

    assert smoothen_path(grid, path, use_raytrace=use_raytrace) == [
        [0, 0], [0, 4], [4, 4], [4, 0]
    ]


@pytest.mark.parametrize('use_raytrace', [False, True])
@pytest.mark.parametrize('path', [[], [[1, 1]], [[0, 0], [1, 0]]])
def test_smoothen_path_short_inputs(path, use_raytrace):
    grid = Grid(width=2, height=2)

    assert smoothen_path(grid, path, use_raytrace=use_raytrace) == path
