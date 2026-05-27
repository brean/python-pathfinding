"""Simple heap with ordering and removal."""
import heapq
from typing import Optional
from .graph import Graph
from .grid import Grid
from .world import World
from .node import Node


class SimpleHeap:
    """Simple wrapper around open_list that keeps track of order."""

    def __init__(self, node, grid):
        self.grid = grid
        self.open_list = [self._get_node_tuple(node, 0)]
        self.number_pushed = 0

    def _get_node_tuple(self, node, heap_order):
        if isinstance(self.grid, Graph):
            return (node.f, heap_order, node.node_id)
        elif isinstance(self.grid, Grid):
            return (node.f, heap_order, node.x, node.y)
        elif isinstance(self.grid, World):
            return (node.f, heap_order, node.x, node.y, node.grid_id)
        else:
            assert False, "unsupported heap node node=%s" % node

    def _get_node_id(self, node):
        if isinstance(self.grid, Graph):
            return node.node_id
        elif isinstance(self.grid, Grid):
            return (node.x, node.y)
        elif isinstance(self.grid, World):
            return (node.x, node.y, node.grid_id)

    def pop_node(self) -> Optional[Node]:
        """Pops node off the heap. i.e. returns the one with the lowest f."""
        while self.open_list:
            node_tuple = heapq.heappop(self.open_list)

            if isinstance(self.grid, Graph):
                node = self.grid.node(node_tuple[2])
            elif isinstance(self.grid, Grid):
                node = self.grid.node(node_tuple[2], node_tuple[3])
            elif isinstance(self.grid, World):
                node = self.grid.grids[
                    node_tuple[4]].node(node_tuple[2], node_tuple[3])
            
            # node already updated with lower f, ignore
            f = node_tuple[0]
            if f > node.f:
                continue
            else:
                return node

        return None

    def push_node(self, node):
        """
        Push node into heap.

        :param node: The node to push.
        """
        self.number_pushed = self.number_pushed + 1
        node_tuple = self._get_node_tuple(node, self.number_pushed)

        heapq.heappush(self.open_list, node_tuple)

    def __len__(self):
        """Returns the length of the open_list."""
        return len(self.open_list)
