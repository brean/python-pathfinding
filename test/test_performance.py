import numpy
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def _add_block(g: numpy.ndarray, x: int, y: int, padding: int):
    for i in range(x - padding, x + padding):
        for j in range(y - padding, y + padding):
            g[j][i] = 0


def test_a_star():
    """Test performance."""
    # Get a 500 x 500 grid
    grid = numpy.ones((500, 500), numpy.int32)

    # Add a block at the center
    _add_block(grid, 250, 250, 50)

    finder_grid = Grid(matrix=grid)
    start = finder_grid.node(0, 0)
    end = finder_grid.node(400, 400)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, finder_grid)

    assert path[0] == start
    assert path[-1] == end
    assert len(path) == 801
