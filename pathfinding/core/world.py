from typing import Dict

from .diagonal_movement import DiagonalMovement
from .grid import Grid
from .node import Node


# a world connects grids but can have multiple grids.
class World:
    def __init__(self, grids: Dict[int, Grid]):
        self.grids = grids

    def neighbors(
        self, node: Node, diagonal_movement: DiagonalMovement
    ) -> list[Node]:
        return self.grids[node.grid_id].neighbors(
            node, diagonal_movement=diagonal_movement)

    def calc_cost(self, node_a, node_b, weighted=False):
        # TODO: if node_a.grid_id != node_b.grid_id calculate distance between
        # grids as well, for now we ignore switching grids
        return self.grids[node_a.grid_id].calc_cost(
            node_a, node_b, weighted=weighted)
