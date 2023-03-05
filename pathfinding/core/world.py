# a world connects grids but can have multiple grids.
class World:
    def __init__(self, grids: dict):
        self.grids = grids

    def neighbors(self, node, diagonal_movement):
        return self.grids[node.grid_id].neighbors(
            node, diagonal_movement=diagonal_movement)
