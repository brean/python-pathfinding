from unittest.mock import patch

from pathfinding.core.graph import Graph
from pathfinding.finder.dijkstra import DijkstraFinder


def test_graph_dijkstra():
    edges = [
        [1, 2, 7],
        [1, 3, 9],
        [1, 6, 14],
        [2, 3, 10],
        [2, 4, 15],
        [3, 4, 11],
        [3, 6, 2],
        [4, 5, 6],
        [6, 5, 9]
    ]

    graph = Graph(edges=edges, bi_directional=True)
    finder = DijkstraFinder()
    path, _ = finder.find_path(graph.node(1), graph.node(5), graph)
    assert [n.node_id for n in path] == [1, 3, 6, 5]


def test_connected_end():
    # see https://github.com/brean/python-pathfinding/issues/51
    edges = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 2, 1],
        [2, 1, 1],
    ]
    graph = Graph(edges=edges, bi_directional=False)
    finder = DijkstraFinder()
    path, _ = finder.find_path(graph.node(0), graph.node(2), graph)
    assert [n.node_id for n in path] == [0, 1, 2]


def test_graph_cleanup():
    graph = Graph(edges=[[0, 1, 1], [1, 0, 1]], bi_directional=False)
    assert not graph.dirty

    finder = DijkstraFinder()
    path, _ = finder.find_path(graph.node(0), graph.node(1), graph)
    assert [n.node_id for n in path] == [0, 1]

    assert graph.dirty

    with patch.object(graph, "cleanup", wraps=graph.cleanup) as mock_cleanup:
        path, _ = finder.find_path(graph.node(1), graph.node(0), graph)
        assert [n.node_id for n in path] == [1, 0]
        mock_cleanup.assert_called_once()
