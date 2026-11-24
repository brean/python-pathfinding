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
        return (node.f, heap_order, node)

    def _get_node_id(self, node):
        if hasattr(node, 'node_id'):
            return node.node_id
        elif hasattr(node, 'grid_id') and node.grid_id is not None:
            return (node.x, node.y, node.grid_id)
        return (node.x, node.y)

    def pop_node(self) -> Optional[Node]:
        """Pops node off the heap. i.e. returns the one with the lowest f."""
        open_list = self.open_list
        while open_list:
            node_tuple = heapq.heappop(open_list)
            node = node_tuple[2]
            # node already updated with lower f, ignore
            if node_tuple[0] > node.f:
                continue
            return node

        return None

    def push_node(self, node):
        """
        Push node into heap.

        :param node: The node to push.
        """
        self.number_pushed += 1
        heapq.heappush(self.open_list, (node.f, self.number_pushed, node))

    def __len__(self):
        """Returns the length of the open_list."""
        return len(self.open_list)

