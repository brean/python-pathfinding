from typing import List
from .diagonal_movement import DiagonalMovement
from .node import GridNode
from ..core.util import SQRT2
try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False


def build_nodes(
        width, height, matrix=None, inverse=False,
        grid_id=None) -> List[List[GridNode]]:
    """
    create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable.
    """
    nodes = []
    use_matrix = (isinstance(matrix, (tuple, list))) or \
        (USE_NUMPY and isinstance(matrix, np.ndarray) and matrix.size > 0)

    min_weight = float("inf")
    for y in range(height):
        nodes.append([])
        for x in range(width):
            # 0, '0', False will be obstacles
            # all other values mark walkable cells.
            # you can use values bigger then 0 to assign a weight.
            # If inverse is False it changes
            # (1 and up becomes obstacle and 0 or everything negative marks a
            #  free cells)
            weight = float(matrix[y][x]) if use_matrix else 1
            walkable = weight <= 0.0 if inverse else weight > 0

            if walkable and weight < min_weight:
                min_weight = weight

            nodes[y].append(GridNode(
                x=x, y=y, walkable=walkable, weight=weight, grid_id=grid_id))

    return nodes, min_weight


class Grid:
    def __init__(
            self, width=0, height=0, matrix=None, grid_id=None,
            inverse=False):
        """
        a grid represents the map (as 2d-list of nodes).
        """
        self.width = width
        self.height = height
        # we will call cleanup automatically if dirty is True
        self.dirty = False
        self.passable_left_right_border = False
        self.passable_up_down_border = False
        if isinstance(matrix, (tuple, list)) or (
                USE_NUMPY and isinstance(matrix, np.ndarray) and (
                matrix.size > 0)):
            self.height = len(matrix)
            self.width = self.width = len(matrix[0]) if self.height > 0 else 0
        if self.width > 0 and self.height > 0:
            self.nodes, self._min_weight = build_nodes(
                self.width, self.height, matrix, inverse, grid_id)
        else:
            self.nodes = [[]]
            self._min_weight = float("inf")

    def set_passable_left_right_border(self):
        self.passable_left_right_border = True

    def set_passable_up_down_border(self):
        self.passable_up_down_border = True

    def node(self, x, y) -> GridNode:
        """
        get node at position
        :param x: x pos
        :param y: y pos
        :return:
        """
        return self.nodes[y][x]

    def inside(self, x, y) -> bool:
        """
        check, if field position is inside map
        :param x: x pos
        :param y: y pos
        :return:
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y) -> bool:
        """
        check, if the tile is inside grid and if it is set as walkable
        """
        return self.inside(x, y) and self.nodes[y][x].walkable

    def calc_cost(self, node_a, node_b, weighted=False):
        """
        get the distance between current node and the neighbor (cost)
        """
        if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
            # direct neighbor - distance is 1
            ng = 1
        else:
            # not a direct neighbor - diagonal movement
            ng = SQRT2

        # weight for weighted algorithms
        if weighted:
            ng *= node_b.weight

        return ng

    def neighbors(
        self, node: GridNode,
        diagonal_movement: DiagonalMovement = DiagonalMovement.never,
        include_non_walkables: bool = False
    ) -> List[GridNode]:
        """
        get all neighbors of one node
        :param node: node
        """
        x = node.x
        y = node.y
        nodes = self.nodes
        neighbors = []
        north = nw = east = ne = south = se = west = sw = False
        width = self.width
        height = self.height
        passable_lr = self.passable_left_right_border
        passable_ud = self.passable_up_down_border

        # ↑
        if y > 0:
            n = nodes[y - 1][x]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                north = True
        elif passable_ud:
            n = nodes[height - 1][x]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                north = True

        # →
        if x + 1 < width:
            n = nodes[y][x + 1]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                east = True
        elif passable_lr:
            n = nodes[y][0]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                east = True

        # ↓
        if y + 1 < height:
            n = nodes[y + 1][x]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                south = True
        elif passable_ud:
            n = nodes[0][x]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                south = True

        # ←
        if x > 0:
            n = nodes[y][x - 1]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                west = True
        elif passable_lr:
            n = nodes[y][width - 1]
            if n.walkable or include_non_walkables:
                neighbors.append(n)
                west = True

        # check for connections to other grids
        if node.connections:
            neighbors.extend(node.connections)

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            nw = north and west
            ne = north and east
            se = south and east
            sw = south and west
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            nw = north or west
            ne = north or east
            se = south or east
            sw = south or west
        elif diagonal_movement == DiagonalMovement.always:
            nw = ne = se = sw = True

        # ↖
        if nw:
            nw_x = width - 1 if (x == 0 and passable_lr) else x - 1
            nw_y = height - 1 if (y == 0 and passable_ud) else y - 1
            if 0 <= nw_x < width and 0 <= nw_y < height:
                n = nodes[nw_y][nw_x]
                if n.walkable or include_non_walkables:
                    neighbors.append(n)

        # ↗
        if ne:
            ne_x = 0 if (x == width - 1 and passable_lr) else x + 1
            ne_y = height - 1 if (y == 0 and passable_ud) else y - 1
            if 0 <= ne_x < width and 0 <= ne_y < height:
                n = nodes[ne_y][ne_x]
                if n.walkable or include_non_walkables:
                    neighbors.append(n)

        # ↘
        if se:
            se_x = 0 if (x == width - 1 and passable_lr) else x + 1
            se_y = 0 if (y == height - 1 and passable_ud) else y + 1
            if 0 <= se_x < width and 0 <= se_y < height:
                n = nodes[se_y][se_x]
                if n.walkable or include_non_walkables:
                    neighbors.append(n)

        # ↙
        if sw:
            sw_x = width - 1 if (x == 0 and passable_lr) else x - 1
            sw_y = 0 if (y == height - 1 and passable_ud) else y + 1
            if 0 <= sw_x < width and 0 <= sw_y < height:
                n = nodes[sw_y][sw_x]
                if n.walkable or include_non_walkables:
                    neighbors.append(n)

        return neighbors

    def cleanup(self):
        for y_nodes in self.nodes:
            for node in y_nodes:
                node.cleanup()

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#',
                 show_weight=False) -> str:
        """
        create a printable string from the grid using ASCII characters

        :param path: list of nodes that show the path
        :param start: start node
        :param end: end node
        :param border: create a border around the grid
        :param start_chr: character for the start (default "s")
        :param end_chr: character for the destination (default "e")
        :param path_chr: character to show the path (default "x")
        :param empty_chr: character for empty fields (default " ")
        :param block_chr: character for blocking elements (default "#")
        :param show_weight: instead of empty_chr show the cost of each empty
                            field (shows a + if the value of weight is > 10)
        :return:
        """
        # create a dict as lookup-table for the path by string for performance
        path_cache = {}
        if path:
            for node in path:
                is_gn = isinstance(node, GridNode)
                x, y = (node.x, node.y) if is_gn else node[:2]
                path_cache[f'{x}_{y}'] = True

        # create the output string
        data = ''
        if border:
            data = f'+{"-" * len(self.nodes[0])}+'
        for y, _ in enumerate(self.nodes):
            line = ''
            for x, _ in enumerate(self.nodes[y]):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and (f'{x}_{y}' in path_cache):
                    line += path_chr
                elif node.walkable:
                    # empty field
                    if node.weight > 10:
                        weight = '+'  # weight bigger than 10
                    elif node.weight < 1 and node.weight > 0:
                        weight = '-'  # weight between 0 and 1
                    else:
                        weight = str(int(node.weight))
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = f'|{line}|'
            if data:
                data += '\n'
            data += line
        if border:
            data += f'\n+{"-" * len(self.nodes[0])}+'
        return data

    def __repr__(self):
        """
        return a human readable representation
        """
        return f"<{self.__class__.__name__} " \
            f"width={self.width} height={self.height}>"

    @property
    def min_weight(self) -> float:
        return self._min_weight

    def update_node(self, x, y, *, weight=None, walkable=None):
        node = self.node(x, y)

        if weight is None:
            weight = node.weight

        if walkable is None:
            walkable = node.walkable

        if walkable:
            if weight <= 0:
                raise ValueError("Weight of a walkable node must be positive")
            if weight < self._min_weight:
                self._min_weight = weight

        node.weight = weight
        node.walkable = walkable
