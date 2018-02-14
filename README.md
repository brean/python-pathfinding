# python-pathfinding
Pathfinding algorithms based on [Pathfinding.JS](https://github.com/qiao/PathFinding.js) for python 2 and 3 (just A* and dijkstra for now)

[![Build Status](https://travis-ci.org/brean/python-pathfinding.svg?branch=master)](https://travis-ci.org/brean/python-pathfinding)
[![Coverage Status](https://coveralls.io/repos/brean/python-pathfinding/badge.svg?branch=master)](https://coveralls.io/r/brean/python-pathfinding?branch=master)

usage example
-------------
A simple usage example to find a path using A*.

1. import the required libraries:
    ```python
    from pathfinding.core.diagonal_movement import DiagonalMovement
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    ```

1. Create a map using a 2D-list. 1, True or any value describes an obstacle. 0, False or None descibes a field that can be walked on. In this example we like the algorithm to create a path from the upper left to the bottom right. To make it not to easy for the algorithm we added an obstacle in the middle, so it can not use the direct way. Feel free to create a more complex map
    ```python
    matrix = [
      [0, 0, 0],
      [0, 1, 0],
      [0, 0, 0]
    ]
    ```

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
    ```
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
  [0, 0, 0],
  [0, 1, 0],
  [0, 0, 0]
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
