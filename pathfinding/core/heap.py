"""Simple heap with ordering and removal."""
import heapq
from .graph import Graph
from .grid import Grid
from .world import World


class SimpleHeap:
    """Simple wrapper around open_list that keeps track of order and removed
    nodes automatically."""

    def __init__(self, node, grid):
        self.grid = grid
        self.open_list = [self._get_node_tuple(node, 0)]
        self.removed_node_tuples = set()
        self.heap_order = {}
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

    def pop_node(self):
        """
        Pops node off the heap. i.e. returns the one with the lowest f.

        Notes:
        1. Checks if that values is in removed_node_tuples first, if not tries
           again.
        2. We use this approach to avoid invalidating the heap structure.
        """
        node_tuple = heapq.heappop(self.open_list)
        while node_tuple in self.removed_node_tuples:
            node_tuple = heapq.heappop(self.open_list)

        if isinstance(self.grid, Graph):
            node = self.grid.node(node_tuple[2])
        elif isinstance(self.grid, Grid):
            node = self.grid.node(node_tuple[2], node_tuple[3])
        elif isinstance(self.grid, World):
            node = self.grid.grids[
                node_tuple[4]].node(node_tuple[2], node_tuple[3])

        return node

    def push_node(self, node):
        """
        Push node into heap.

        :param node: The node to push.
        """
        self.number_pushed = self.number_pushed + 1
        node_tuple = self._get_node_tuple(node, self.number_pushed)
        node_id = self._get_node_id(node)

        self.heap_order[node_id] = self.number_pushed

        heapq.heappush(self.open_list, node_tuple)

    def remove_node(self, node, f):
        """
        Remove the node from the heap.

        This just stores it in a set and we just ignore the node if it does
        get popped from the heap.

        :param node: The node to remove.
        :param f: The old f value of the node.
        """
        node_id = self._get_node_id(node)
        heap_order = self.heap_order[node_id]
        node_tuple = self._get_node_tuple(node, heap_order)
        self.removed_node_tuples.add(node_tuple)

    def __len__(self):
        """Returns the length of the open_list."""
        return len(self.open_list)
