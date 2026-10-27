import pytest

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.ida_star import IDAStarFinder


DIAGONALS = [
    DiagonalMovement.never,
    DiagonalMovement.always,
    DiagonalMovement.if_at_most_one_obstacle,
    DiagonalMovement.only_when_no_obstacle,
]


@pytest.mark.parametrize("diagonal", DIAGONALS)
@pytest.mark.parametrize("track_recursion", [False, True])
@pytest.mark.parametrize("matrix,end", [
    ([[1, 0, 1]], (2, 0)),
    ([[1, 1, 1, 0, 1]], (4, 0)),
    ([[1, 1, 0, 1], [1, 1, 0, 1]], (3, 1)),
])
def test_unreachable_destination_finishes(matrix, end, diagonal,
                                        track_recursion):
    grid = Grid(matrix=matrix)
    finder = IDAStarFinder(diagonal_movement=diagonal,
                           track_recursion=track_recursion, max_runs=1000)
    path, runs = finder.find_path(grid.node(0, 0), grid.node(*end), grid)
    assert path == []
    assert 0 < runs < 1000


@pytest.mark.parametrize("diagonal", DIAGONALS)
@pytest.mark.parametrize("track_recursion", [False, True])
def test_search_can_be_reused_after_unreachable_destination(diagonal,
                                                           track_recursion):
    grid = Grid(matrix=[[1, 1, 0, 1], [1, 1, 0, 1]])
    finder = IDAStarFinder(diagonal_movement=diagonal,
                           track_recursion=track_recursion, max_runs=1000)
    start = grid.node(0, 0)
    assert finder.find_path(start, grid.node(3, 1), grid)[0] == []
    path, _ = finder.find_path(start, grid.node(1, 1), grid)
    assert path[0] is start
    assert path[-1] is grid.node(1, 1)
    assert len(path) == (3 if diagonal == DiagonalMovement.never else 2)
    assert len({id(node) for node in path}) == len(path)
