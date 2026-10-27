import pytest

from pathfinding.core.grid import Grid
from pathfinding.finder import msp
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.finder import (
    ExecutionRunsException, ExecutionTimeException,
)
from pathfinding.finder.msp import MinimumSpanningTree


@pytest.mark.parametrize('method', ['tree', 'itertree'])
def test_tree_initializes_time_limit(method, monkeypatch):
    monkeypatch.setattr(msp.time, 'time', lambda: 100)
    grid = Grid(matrix=[[1, 1, 1]])
    finder = MinimumSpanningTree(time_limit=10)

    nodes = list(getattr(finder, method)(grid, grid.node(0, 0)))

    assert [node.x for node in nodes] == [0, 1, 2]
    assert finder.runs == 3


@pytest.mark.parametrize('method', ['tree', 'itertree'])
@pytest.mark.parametrize('reuse_finder', [False, True])
def test_tree_can_reuse_grid(method, reuse_finder):
    grid = Grid(matrix=[[1, 1, 1]])
    finder = MinimumSpanningTree()
    assert len(list(getattr(finder, method)(grid, grid.node(0, 0)))) == 3
    if not reuse_finder:
        finder = MinimumSpanningTree()

    nodes = list(getattr(finder, method)(grid, grid.node(2, 0)))

    assert [node.x for node in nodes] == [2, 1, 0]
    assert [node.g for node in nodes] == [0, 1, 2]
    assert nodes[0].parent is None
    assert finder.runs == 3


@pytest.mark.parametrize('method', ['tree', 'itertree'])
@pytest.mark.parametrize('tree_first', [False, True])
def test_tree_and_path_search_can_share_grid(method, tree_first):
    grid = Grid(matrix=[[1, 1, 1]])
    start, end = grid.node(0, 0), grid.node(2, 0)
    finder = MinimumSpanningTree()
    if tree_first:
        assert len(list(getattr(finder, method)(grid, start))) == 3
        path, _ = AStarFinder().find_path(end, start, grid)
        assert [node.x for node in path] == [2, 1, 0]
    else:
        path, _ = AStarFinder().find_path(start, end, grid)
        assert [node.x for node in path] == [0, 1, 2]
        nodes = list(getattr(finder, method)(grid, end))
        assert [node.x for node in nodes] == [2, 1, 0]
        assert [node.g for node in nodes] == [0, 1, 2]


@pytest.mark.parametrize('method', ['tree', 'itertree'])
def test_tree_resets_run_budget(method):
    grid = Grid(matrix=[[1, 1, 1]])
    finder = MinimumSpanningTree(max_runs=4)
    for _ in range(2):
        nodes = list(getattr(finder, method)(grid, grid.node(0, 0)))
        assert len(nodes) == 3
        assert finder.runs == 3


def test_tree_can_restart_after_partial_iteration():
    grid = Grid(matrix=[[1, 1, 1]])
    finder = MinimumSpanningTree()
    iterator = finder.itertree(grid, grid.node(0, 0))
    assert next(iterator) is grid.node(0, 0)
    iterator.close()

    nodes = finder.tree(grid, grid.node(2, 0))

    assert [node.x for node in nodes] == [2, 1, 0]
    assert finder.runs == 3


def test_tree_run_limit_still_applies():
    grid = Grid(matrix=[[1, 1, 1]])
    finder = MinimumSpanningTree(max_runs=2)
    with pytest.raises(ExecutionRunsException):
        finder.tree(grid, grid.node(0, 0))


def test_tree_time_limit_still_applies(monkeypatch):
    clock = iter([100, 101, 111])
    monkeypatch.setattr(msp.time, 'time', lambda: next(clock))
    grid = Grid(matrix=[[1, 1, 1]])
    iterator = MinimumSpanningTree(time_limit=10).itertree(
        grid, grid.node(0, 0))

    assert next(iterator) is grid.node(0, 0)
    with pytest.raises(ExecutionTimeException):
        next(iterator)


def test_spanning_tree_find_path_still_resets_state():
    grid = Grid(matrix=[[1, 2, 3]])
    finder = MinimumSpanningTree()
    for start_x, end_x, expected in [(0, 2, [0, 1, 2]), (2, 0, [2, 1, 0])]:
        path, runs = finder.find_path(
            grid.node(start_x, 0), grid.node(end_x, 0), grid)
        assert [node.x for node in path] == expected
        assert runs == 3
