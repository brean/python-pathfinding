# Using a graph
The default is to plan a path from one node of a grid to another but you can use any graph that has a weight (also known as cost) assigned to its edges.

```python
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.graph import Graph
from pathfinding.core.node import Node
from pathfinding.finder.a_star import AStarFinder

# based on the animation at [Wikipedia about Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#/media/File:Dijkstra_Animation.gif)

# source node, target node, distance value
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
```
the `path` holds the list of nodes to move to in order. Instead of numbers you can also use strings (e.g. waypoint or city names)

