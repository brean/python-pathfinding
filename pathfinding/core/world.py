from typing import Dict

from .grid import Grid
from .node import Node
from .diagonal_movement import DiagonalMovement

# a world connects grids but can have multiple grids.
class World:
    def __init__(self, grids: Dict[int, Grid]):
        self.grids = grids

    def neighbors(self, node: Node, diagonal_movement: DiagonalMovement):
        return self.grids[node.grid_id].neighbors(
            node, diagonal_movement=diagonal_movement)
