# steps/elevators/portals
*python-pathfinding* allows you to connect grids. This could be useful to create buildings with multiple storeys that are connected by elevators or stairs or different areas you want to connect with portals.

Lets say we want to connect 2 level with 
an elevator or steps you start to :
```python
level0 = [
  [1, 1, 1],
  [1, 0, 0],
  [1, 1, 1]
]
level1 = [
  [1, 1, 1],
  [0, 0, 1],
  [1, 1, 1]
]
# create Grid instances for both level
grid0 = Grid(matrix=level0, grid_id=0)
grid1 = Grid(matrix=level1, grid_id=1)
```

We can connect a node from one grid to another by defining a connection between the two grids like this:
```python
# elevator up
grid0.node(2, 2).connect(grid1.node(2, 2))
# elevator down
grid1.node(2, 2).connect(grid0.node(2, 2))
```

Note that we need to do this in both directions if we want to allow the connection to go both ways.

Because the `find_neighbors`-function in the finder needs to look up both grids we need to provide both grids to the finder. We can create a "world" that looks up both grids:

```python
  # create world with both grids
world = World({
    0: grid0,
    1: grid1
})

finder = AStarFinder()
path, _ = finder.find_path(grid0.node(2, 0), grid1.node(0, 0), world)
```

for the whole code take a look at the `test_connect_grids.py` file in the `test`-folder