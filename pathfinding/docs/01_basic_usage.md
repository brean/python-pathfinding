# Basic usage

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

Here is the whole example if you just want to copy-and-paste the code and play with it:

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