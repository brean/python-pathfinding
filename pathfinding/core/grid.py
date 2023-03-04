# -*- coding: utf-8 -*-
from .diagonal_movement import DiagonalMovement
from .node import Node
try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False


# clockwise rotation around current node
NORTH = 0b1
WEST = 0b10
SOUTH = 0b100
EAST = 0b1000
# ...and for diagonal movement
NORTH_WEST = 0b10000
SOUTH_WEST = 0b100000
SOUTH_EAST = 0b1000000
NORTH_EAST = 0b10000000
# all neighbors are walkable
AROUND = 0b11111111
OPPOSITE = {
    NORTH: SOUTH,
    WEST: EAST,
    SOUTH: NORTH,
    EAST: WEST,
    NORTH_WEST: SOUTH_EAST,
    SOUTH_WEST: NORTH_EAST,
    SOUTH_EAST: NORTH_WEST,
    NORTH_EAST: SOUTH_WEST,
}


def build_nodes(width, height, matrix=None, inverse=False, border=None):
    """
    create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable.
    :rtype : list
    """
    nodes = []
    use_matrix = (isinstance(matrix, (tuple, list))) or \
        (USE_NUMPY and isinstance(matrix, np.ndarray) and matrix.size > 0)

    for y in range(height):
        nodes.append([])
        for x in range(width):
            # 0, '0', False will be obstacles
            # all other values mark walkable cells.
            # you can use values bigger then 1 to assign a weight.
            # If inverse is False it changes
            # (1 and up becomes obstacle and 0 or everything negative marks a
            #  free cells)
            weight = int(matrix[y][x]) if use_matrix else 1
            walkable = weight <= 0 if inverse else weight >= 1
            _border = border[y][x] if border else AROUND

            nodes[y].append(Node(
                x=x, y=y, walkable=walkable, weight=weight, border=_border))
    return nodes


class Grid(object):
    def __init__(
            self, width=0, height=0, matrix=None, inverse=False,
            border=None):
        """
        a grid represents the map (as 2d-list of nodes).

        :param width: width of the grid. Calculated if a matrix is given.
        :param height: height of the grid. Calculated if a matrix is given.
        :param matrix: 2d-tuple or 2d-list of numbers representing cost
        :param inverse: positive values in the matrix are walkable
          if it is false (default), otherwise negative alues are walkable
        :param borders: a 2d-tuple or 2d-list with the same size as the matrix
          but the values represent the borders in binary
        """
        self.width = width
        self.height = height
        self.passable_left_right_border = False
        self.passable_up_down_border = False
        if isinstance(matrix, (tuple, list)) or (
                USE_NUMPY and isinstance(matrix, np.ndarray) and
                matrix.size > 0):
            self.height = len(matrix)
            self.width = self.width = len(matrix[0]) if self.height > 0 else 0
        if self.width > 0 and self.height > 0:
            self.nodes = build_nodes(
                self.width, self.height, matrix, inverse, border=border)
        else:
            self.nodes = [[]]

    def set_passable_left_right_border(self):
        self.passable_left_right_border = True

    def set_passable_up_down_border(self):
        self.passable_up_down_border = True

    def node(self, x, y):
        """
        get node at position
        :param x: x pos
        :param y: y pos
        :return:
        """
        return self.nodes[y][x]

    def inside(self, x, y):
        """
        check, if field position is inside map
        :param x: x pos
        :param y: y pos
        :return:
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y, from_x=None, from_y=None, direction=AROUND):
        """
        check, if the tile is inside grid and if it is set as walkable
        """
        if not self.inside(x, y):
            return False

        to_node = self.node(x, y)
        # check if move from node at xy to this position is possible
        # according to border-grid stored in the node.
        if from_x and from_y and not\
                self.node(from_x, from_y).border & direction:
            return False
        # also check the other direction
        if direction != AROUND:
            if not to_node.border & OPPOSITE[direction]:
                return False

        return to_node.walkable

    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        """
        get all neighbors of one node
        :param node: node
        """
        x = node.x
        y = node.y
        neighbors = []
        straight_north = straight_east = straight_south = straight_west =\
            diag_nw = diag_ne = diag_se = diag_sw = False

        # ↑
        if y == 0 and self.passable_up_down_border:
            if self.walkable(x, self.height - 1):
                neighbors.append(self.nodes[self.height - 1][x])
                straight_north = True
        else:
            if self.walkable(x, y - 1, x, y, NORTH):
                neighbors.append(self.nodes[y - 1][x])
                straight_north = True
        # →
        if x == self.width - 1 and self.passable_left_right_border:
            if self.walkable(0, y):
                neighbors.append(self.nodes[y][0])
                straight_east = True
        else:
            if self.walkable(x + 1, y, WEST):
                neighbors.append(self.nodes[y][x + 1])
                straight_east = True
        # ↓
        if y == self.height - 1 and self.passable_up_down_border:
            if self.walkable(x, 0):
                neighbors.append(self.nodes[0][x])
                straight_south = True
        else:
            if self.walkable(x, y + 1, x, y, SOUTH):
                neighbors.append(self.nodes[y + 1][x])
                straight_south = True
        # ←
        if x == 0 and self.passable_left_right_border:
            if self.walkable(self.width - 1, y):
                neighbors.append(self.nodes[y][self.width - 1])
                straight_west = True
        else:
            if self.walkable(x - 1, y, x, y, EAST):
                neighbors.append(self.nodes[y][x - 1])
                straight_west = True

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            diag_nw = straight_west and straight_north
            diag_ne = straight_north and straight_east
            diag_se = straight_east and straight_south
            diag_sw = straight_south and straight_west
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            diag_nw = straight_west or straight_north
            diag_ne = straight_north or straight_east
            diag_se = straight_east or straight_south
            diag_sw = straight_south or straight_west
        elif diagonal_movement == DiagonalMovement.always:
            diag_nw = diag_ne = diag_se = diag_sw = True

        # ↖
        if diag_nw and self.walkable(x - 1, y - 1, x, y, NORTH_WEST):
            neighbors.append(self.nodes[y - 1][x - 1])

        # ↗
        if diag_ne and self.walkable(x + 1, y - 1, x, y, NORTH_EAST):
            neighbors.append(self.nodes[y - 1][x + 1])

        # ↘
        if diag_se and self.walkable(x + 1, y + 1, x, y, SOUTH_EAST):
            neighbors.append(self.nodes[y + 1][x + 1])

        # ↙
        if diag_sw and self.walkable(x - 1, y + 1, x, y, SOUTH_WEST):
            neighbors.append(self.nodes[y + 1][x - 1])

        return neighbors

    def cleanup(self):
        for y_nodes in self.nodes:
            for node in y_nodes:
                node.cleanup()

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#',
                 show_weight=False):
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
        data = ''
        if border:
            data = '+{}+'.format('-' * len(self.nodes[0]))
        for y in range(len(self.nodes)):
            line = ''
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and ((node.x, node.y) in path or node in path):
                    line += path_chr
                elif node.walkable:
                    # empty field
                    weight = str(node.weight) if node.weight < 10 else '+'
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = '|' + line + '|'
            if data:
                data += '\n'
            data += line
        if border:
            data += '\n+{}+'.format('-' * len(self.nodes[0]))
        return data
