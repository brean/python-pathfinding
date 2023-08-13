# python-pathfinding

Pathfinding algorithms for python 3.

Currently there are 7 path-finders bundled in this library, namely:

- A*
- Dijkstra
- Best-First
- Bi-directional A*
- Breadth First Search (BFS)
- Iterative Deeping A\* (IDA*)
- Minimum Spanning Tree (MSP)

Dijkstra and A* take the weight of the fields on the map into account.

![MIT License](https://img.shields.io/github/license/brean/python-pathfinding)
![PyPI](https://img.shields.io/pypi/v/pathfinding)

*If you are still using python 2 take a look at the [python2-branch](https://github.com/brean/python-pathfinding/tree/python2).*

## Installation

This library is provided by pypi, so you can just install the current stable version using pip:

```python
pip install pathfinding
```

see [pathfinding on pypi](https://pypi.org/project/pathfinding/)

## Usage examples
For usage examples with detailed descriptions take a look at the [docs](docs/) folder, also take a look at the [test/](test/) folder for more examples, e.g. how to use pandas

## Rerun the algorithm

While running the pathfinding algorithm it might set values on the nodes. Depending on your path finding algorithm things like calculated distances or visited flags might be stored on them. So if you want to run the algorithm in a loop you need to clean the grid first (see `Grid.cleanup`). Please note that because cleanup looks at all nodes of the grid it might be an operation that can take a bit of time!

## Implementation details

All pathfinding algorithms in this library are inheriting the Finder class. It has some common functionality that can be overwritten by the implementation of a path finding algorithm.

The normal process works like this:

1. You call `find_path` on one of your finder implementations.
1. `init_find` instantiates the `open_list` and resets all values and counters.
1. The main loop starts on the `open_list`. This list gets filled with all nodes that will be processed next (e.g. all current neighbors that are walkable). For this you need to implement `check_neighbors` in your own finder implementation.
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

## Testing
You can run the tests locally using pytest. Take a look at the `test`-folder

## Contributing

Please use the [issue tracker](https://github.com/brean/python-pathfinding/issues) to submit bug reports and feature requests. Please use merge requests as described [here](/CONTRIBUTING.md) to add/adapt functionality. 

## License

python-pathfinding is distributed under the [MIT license](https://opensource.org/licenses/MIT).

## Maintainer

Andreas Bresser, self@andreasbresser.de

## Authors / Contributers
Authors and contributers are [listed on github](https://github.com/brean/python-pathfinding/graphs/contributors).

Inspired by [Pathfinding.JS](https://github.com/qiao/PathFinding.js)