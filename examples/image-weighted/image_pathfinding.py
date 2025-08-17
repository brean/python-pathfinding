# Create a Map from an image
import os
from pathlib import Path
import argparse
from random import uniform as random_float

# Pillow
from PIL import Image

# pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


# image file with the map
BASE_PATH = Path(os.path.dirname(__file__))
MAP_FILE = BASE_PATH / "map.png"
OUT_FILE = BASE_PATH / "out.png"

# this script searches for specific colors in RGB-format
COLOR_START = (255, 255, 0)  # yellow
COLOR_END = (255, 0, 0)  # red
COLOR_PATH = (255, 165, 0)  # orange
COLOR_WEIGHT_MAPPING = {
    (0, 62, 178): 10,  # deep water
    (9, 82, 198): 3,  # water
    (254, 224, 179): 1,  # sand
    (9, 120, 93): 2,  # grass
    (10, 107, 72): 3,  # bushes
    (11, 94, 51): 4,  # forest
    (140, 142, 123): 5,  # hills
    (160, 162, 143): 10,  # alpine
    (53, 54, 68): 15,  # steep cliff
    (255, 255, 255): 10,  # snow
}


def main(filename_map: str = MAP_FILE, filename_out: str = OUT_FILE, weight_randomization: float = 0):
    nodes = []
    if not Path(filename_map).exists():
        print(f'File {filename_map} does not exist.')
        return

    print('Parsing map..')
    with Image.open(filename_map) as im:
        width, height = im.size
        for y in range(height):
            nodes.append([])
            for x in range(width):
                pixel = im.getpixel((x, y))
                weight = COLOR_WEIGHT_MAPPING.get(pixel, 1)

                if weight_randomization != 0:
                    weight += random_float(0, weight_randomization)

                nodes[y].append(weight)

                if pixel == COLOR_END:
                    _goal = (x, y)
                elif pixel == COLOR_START:
                    _start = (x, y)

        grid = Grid(matrix=nodes)
        end = grid.node(*_goal)
        start = grid.node(*_start)

        print('Finding optimal path..')
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)

        # print(grid.grid_str(path=path, end=end, start=start))
        print(f'iterations: {runs:_} path length: {len(path):_}')

        print('Saving image..')
        out = im.copy()
        for p in path[1:-1]:
            out.putpixel((p.x, p.y), COLOR_PATH)
        out.save(filename_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='image_pathfinding',
        description='find a path in an image from a yellow pixel (rgb: 255,255,0) to a red one (rgb: 255,0,0) '
                    'with weighted-tiles')
    parser.add_argument(
        '-i', '--filename_map',
        help='input file',
        default=MAP_FILE)
    parser.add_argument(
        '-o', '--filename_out',
        help='output file',
        default=OUT_FILE)
    parser.add_argument(
        '-r', '--weight-randomization',
        help='how much randomization should be added to the tile-weights (disabled by default)',
        type=float,
        default=0)

    main(**vars(parser.parse_args()))
