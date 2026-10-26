import pytest

from pathfinding.core.grid import Grid
from pathfinding.core.util import expand_path


@pytest.mark.parametrize('path, expected', [
    ([], []),
    ([[2, 3]], []),
    ([[0, 0], [3, 0]], [[0, 0], [1, 0], [2, 0], [3, 0]]),
    ([[2, 2], [0, 0]], [[2, 2], [1, 1], [0, 0]]),
    ([[0, 0], [2, 0], [2, 2]],
     [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]),
    ([[0, 0], [0, 0], [2, 0]], [[0, 0], [1, 0], [2, 0]]),
    ([[1, 1], [1, 1]], [[1, 1]]),
    ([[0, 0], [2, 0], [0, 0]],
     [[0, 0], [1, 0], [2, 0], [1, 0], [0, 0]]),
])
def test_expand_path(path, expected):
    assert expand_path(path) == expected


def test_expand_path_tuple_coordinates():
    assert expand_path([(0, 0), (0, 2), (2, 2)]) == [
        [0, 0], [0, 1], [0, 2], [1, 2], [2, 2]
    ]


def test_expanded_path_can_be_rendered_on_grid():
    grid = Grid(width=4, height=1)
    expanded = expand_path([[0, 0], [3, 0]])

    assert grid.grid_str(path=expanded, border=False) == 'xxxx'
