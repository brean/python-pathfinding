# 1.0.17
## Bugfix
- fix for Graph: Error when running pathfinding multiple times in graph. (see #67)

## General
- updated documentation for benchmarking
- add more type definitions

# 1.0.16
## Bugfix
- fix for ida_star: visualize all visited nodes, not just the last one.

# 1.0.15
## Bugfix
- fix for ida_star: return list of nodes instead of x-y-tuples

# 1.0.14
## Bugfix
- fix heuristic in a weighted graph (see #65, merges #66)

# 1.0.13
## Features/Bugfix
- allow for path finding with float values as cost.

# 1.0.12
## Bugfixes
- fix for passable borders (see #62, merges #63)

# 1.0.11
## Bugfixes
- always call cleanup
- cleanup worlds
- return empty on msp

# 1.0.10
## Bugfixes
- allow diagonal crossing movement over a border (see #58)
- fix import in documentation for graphs

# 1.0.9
## Bugifxes
- update return type annoation (see #55)

# 1.0.8
## Performance
- huge performance update by reducing lookup time for smallest entry in heapq. (see #53, thanks to @peterchenadded)

# 1.0.7
## Bugfixes
- fixed calculation of graph width (see #52)

# 1.0.6
## Bugfixes
- removed an unused debug print that lead to performance issues on big maps

# 1.0.5
## Bugfixes
- fixed a bug for graphs where node_ids were not unique (#51)

# 1.0.4
## Bugfixes
- backward-compability with Python 3.9

# 1.0.3
## Bugfixes
- lookup-table/cache for the path in grid_str for faster output.

## New features
- Support for generic graphs that are not grids.

## General
- Minor PEP 8 fixes, (import order, remove empty lines, remove utf-8 force because it's the default in Python3)

# 1.0.2
## New features
- portals/elevators/steps (see [docs/02_connecting_grids.md](docs/02_connecting_grids.md))

## Security
- update Pipfile.lock (had depenencies on vulnerable pytest version)

## General
- **BREAKING CHANGE** remove Python 2 support (for older Python 3 and Python 2 see python2-branch)
- **BREAKING CHANGE** Node is a dataclass now
- stricter flake8 integration
- moved usage documentation to [docs](docs/)
- add contributing and changelog
- update license to 2023

# 1.0.1
## Bugfixes
- fix super call in Minimum Spanning Tree

# 1.0.0
## New features
- add Minimum Spanning Tree

## General
- throw error when check_neighbors isn't implemented
- add badges
- fix spelling, typos and update text in Readme
- update License to 2020

# 0.4.0
## Bugfix
- fix calc_cost (cost was calculated incorrectly)

## General
- add pipenv Pipfile

# 0.3.0
## Bugfix
- add long description from README.md to setup.py

## General
- More documentation and typo fixes

# 0.2.0
## Bugfixes
- use copy.copy for python2.5
- cleanup grid instead of recreate it every time (see #9)
- **BEHAVIOR CHANGED** Switch node walkable flag to use it as weight, so <0 is an obstacle and >=1 is a walkable field now

## New features
- BestFirstSearch (BFS)
- raytrace for path smoothing
- weighted path finding for A* and Dijkstra

## General
- coveralls integration
- removed debug logs
- updated license to 2018
- More unit tests, add constrains for time and step count
- flake8 integration

# 0.1.0
Initial release