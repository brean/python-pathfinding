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
    path, runs = finder.find_path(graph.node(1), graph.node(5), graph)
    assert [n.node_id for n in path] == [1, 3, 6, 5]
