import pytest

from pathfinding.core.grid import Grid
from pathfinding.core.world import World
from pathfinding.finder.bi_a_star import BiAStarFinder
from pathfinding.finder.bi_best_first import BiBestFirstFinder
from pathfinding.finder.bi_breadth_first import BiBreadthFirstFinder
from pathfinding.finder.bi_dijkstra import BiDijkstraFinder


bidirectional_finders = [
    BiAStarFinder, BiBestFirstFinder, BiBreadthFirstFinder, BiDijkstraFinder,
]


@pytest.mark.parametrize('finder_class', bidirectional_finders)
@pytest.mark.parametrize('matrix,point', [
    ([[1]], (0, 0)),
    ([[1, 1], [1, 1]], (0, 0)),
    ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], (1, 1)),
])
def test_bidirectional_same_endpoint(finder_class, matrix, point):
    grid = Grid(matrix=matrix)
    node = grid.node(*point)
    finder = finder_class()

    path, runs = finder.find_path(node, node, grid)

    assert len(path) == 1
    assert path[0] is node
    assert runs == 0
    assert finder.runs == 0


@pytest.mark.parametrize('finder_class', bidirectional_finders)
def test_bidirectional_same_endpoint_between_normal_searches(finder_class):
    grid = Grid(matrix=[[1, 1, 1]])
    start = grid.node(0, 0)
    end = grid.node(2, 0)
    finder = finder_class()

    path, runs = finder.find_path(start, end, grid)
    assert [(node.x, node.y) for node in path] == [(0, 0), (1, 0), (2, 0)]
    assert runs > 0

    path, runs = finder.find_path(end, end, grid)
    assert len(path) == 1
    assert path[0] is end
    assert runs == 0
    assert end.parent is None

    path, runs = finder.find_path(end, start, grid)
    assert [(node.x, node.y) for node in path] == [(2, 0), (1, 0), (0, 0)]
    assert runs > 0


@pytest.mark.parametrize('finder_class', bidirectional_finders)
def test_same_coordinates_in_different_grids_are_distinct(finder_class):
    first = Grid(matrix=[[1]], grid_id=0)
    second = Grid(matrix=[[1]], grid_id=1)
    start = first.node(0, 0)
    end = second.node(0, 0)
    start.connect(end)
    end.connect(start)
    world = World({0: first, 1: second})

    path, runs = finder_class().find_path(start, end, world)

    assert len(path) == 2
    assert path[0] is start
    assert path[1] is end
    assert runs > 0
