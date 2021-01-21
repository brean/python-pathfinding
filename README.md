# python-pathfinding

Pathfinding algorithms for python 2 and 3.

Currently there are 7 path-finders bundled in this library, namely:

- A*
- Dijkstra
- Best-First
- Bi-directional A*
- Breadth First Search (BFS)
- Iterative Deeping A\* (IDA*)
- Minimum Spanning Tree (MSP)

Dijkstra and A* take the weight of the fields on the map into account.

[![Build Status](https://travis-ci.org/brean/python-pathfinding.svg?branch=master)](https://travis-ci.org/brean/python-pathfinding)
[![Coverage Status](https://coveralls.io/repos/github/brean/python-pathfinding/badge.svg?branch=master)](https://coveralls.io/github/brean/python-pathfinding?branch=master)
![MIT License](https://img.shields.io/github/license/brean/python-pathfinding)
![PyPI](https://img.shields.io/pypi/v/pathfinding)

Inspired by [Pathfinding.JS](https://github.com/qiao/PathFinding.js)

## Installation

This library is provided by pypi, so you can just install the current stable version using pip:

```python
pip install pathfinding
```

see [pathfinding on pypi](https://pypi.org/project/pathfinding/)

## Usage example

A simple usage example to find a path using A*.

1. import the required libraries:

    ```python
    from pathfinding.core.diagonal_movement import DiagonalMovement
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    ```

1. Create a map using a 2D-list. Any value smaller or equal to 0 describes an obstacle. Any number bigger than 0 describes the weight of a field that can be walked on. The bigger the number the higher the cost to walk that field. In this example we like the algorithm to create a path from the upper left to the bottom right. To make it not to easy for the algorithm we added an obstacle in the middle, so it can not use the direct way. We ignore the weight for now, all fields have the same cost of 1. Feel free to create a more complex map or use some sensor data as input for it.

    ```python
    matrix = [
      [1, 1, 1],
      [1, 0, 1],
      [1, 1, 1]
    ]
    ```

  Note: you can use negative values to describe different types of obstacles. It does not make a difference for the path finding algorithm but it might be useful for your later map evaluation.

1. we create a new grid from this map representation. This will create Node instances for every element of our map. It will also set the size of the map. We assume that your map is a square, so the size height is defined by the length of the outer list and the width by the length of the first list inside it.

    ```python
    grid = Grid(matrix=matrix)
    ```

1. we get the start (top-left) and endpoint (bottom-right) from the map:

    ```python
    start = grid.node(0, 0)
    end = grid.node(2, 2)
    ```

1. create a new instance of our finder and let it do its work. We allow diagonal movement. The `find_path` function does not only return you the path from the start to the end point it also returns the number of times the algorithm needed to be called until a way was found.

    ```python
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    ```

1. thats it. We found a way. Now we can print the result (or do something else with it). Note that the start and end points are part of the path.

    ```python
    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    ```

    The result should look like this:

    ```pseudo
    ('operations:', 5, 'path length:', 4)

    +---+
    |sx |
    | #x|
    |  e|
    +---+
    ```

    You can ignore the +, - and | characters, they just show the border around your map, the blank space is a free field, 's' marks the start, 'e' the end and '#' our obstacle in the middle. You see the path from start to end marked by 'x' characters. We allow horizontal movement, so it is not using the upper-right corner. You can access `print(path)` to get the specific list of coordinates.

Here The whole example if you just want to copy-and-paste the code and play with it:

```python
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

matrix = [
  [1, 1, 1],
  [1, 0, 1],
  [1, 1, 1]
]
grid = Grid(matrix=matrix)

start = grid.node(0, 0)
end = grid.node(2, 2)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print(grid.grid_str(path=path, start=start, end=end))
```

Take a look at the _`test/`_ folder for more examples.

## Rerun the algorithm

While running the pathfinding algorithm it might set values on the nodes. Depending on your path finding algorithm things like calculated distances or visited flags might be stored on them. So if you want to run the algorithm in a loop you need to clean the grid first (see `Grid.cleanup`). Please note that because cleanup looks at all nodes of the grid it might be an operation that can take a bit of time!

## Implementation details

All pathfinding algorithms in this library are inheriting the Finder class. It has some common functionality that can be overwritten by the implementation of a path finding algorithm.

The normal process works like this:

1. You call `find_path` on one of your finder implementations
1. `init_find` instantiates `open_list` and resets all values and counters.
1. The main loop starts on the `open_list`. This list gets filled with all nodes that will be processed next (e.g. all neighbors that are walkable). For this you need to implement `check_neighbors` in your own finder implementation.
1. For example in A*s implementation of `check_neighbors` you first want to get the next node closest from the current starting point from the open list. the `next_node` method in Finder does this by giving you the node with a minimum `f`-value from the open list, it closes it and removes it from the `open_list`.
1. if this node is not the end node we go on and get its neighbors by calling `find_neighbors`. This just calls `grid.neighbors` for most algorithms.
1. If none of the neighbors are the end node we want to process the neighbors to calculate their distances in `process_node`
1. `process_node` calculates the cost `f` from the start to the current node using the `calc_cost` method and the cost after calculating `h` from `apply_heuristic`.
1. finally `process_node` updates the open list so `find_path` can run `check_neighbors` on it in the next node in the next iteration of the main loop.

flow:

```pseudo
  find_path
    init_find  # (re)set global values and open list
    check_neighbors  # for every node in open list
      next_node  # closest node to start in open list
      find_neighbors  # get neighbors
      process_node  # calculate new cost for neighboring node
```
