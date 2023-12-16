from enum import Enum
import sys

sys.setrecursionlimit(1000000)

# Definitions used as bitmasks
ILLUM_NONE = 0
ILLUM_NS = 1
ILLUM_EW = 2
ILLUM_BOTH = 3
ILLUM_MIRROR_NORTH = 1 << 2
ILLUM_MIRROR_WEST = 2 << 2
ILLUM_MIRROR_SOUTH = 3 << 2
ILLUM_MIRROR_EAST = 4 << 2
ILLUM_SPLIT_THROUGH = 1 << 5
ILLUM_SPLIT_SPLIT = 2 << 5

# Enums
class MapElement(Enum):
    EMPTY = 0
    SLASH_MIRROR = 1
    BACKSLASH_MIRROR = 2
    H_SPLITTER = 3
    V_SPLITTER = 4

class Direction(Enum):
    NORTH = (-1, 0, ILLUM_NS)
    WEST = (0, -1, ILLUM_EW)
    SOUTH = (1, 0, ILLUM_NS)
    EAST = (0, 1, ILLUM_EW)

class MapNode:
    def __init__(self, element: MapElement, illumination: int) -> None:
        self.element = element
        self.illumination = illumination

    def add_illumination(self, new_illumination: int) -> None:
        self.illumination |= new_illumination

def project_beam(row: int, col: int, dir: Direction, map: [[MapNode]]):
    # End recursion if out of the map bounds
    if row < 0 or row >= len(map):
        return
    if col < 0 or col >= len(map[0]):
        return
    
    map_node = map[row][col]

    # End recursion if this duplicates existing illumination
    if dir == Direction.NORTH or dir == Direction.SOUTH:
        if (map_node.illumination & ILLUM_NS) == ILLUM_NS:
            return
    if dir == Direction.EAST or dir == Direction.WEST:
        if (map_node.illumination & ILLUM_EW) == ILLUM_EW:
            return
    
    # Switch based on what's at this location, illuminate, and recur.
    if map_node.element == MapElement.EMPTY:
        map_node.illumination |= dir.value[2]
        project_beam(row + dir.value[0], col + dir.value[1], dir, map)
    if map_node.element == MapElement.SLASH_MIRROR:
        # Mirror /
        # Project the beam based on the direction
        if dir == Direction.NORTH:
            map_node.illumination = ILLUM_MIRROR_NORTH
            project_beam(row, col + 1, Direction.EAST, map)
        elif dir == Direction.WEST:
            map_node.illumination = ILLUM_MIRROR_WEST
            project_beam(row + 1, col, Direction.SOUTH, map)
        elif dir == Direction.SOUTH:
            map_node.illumination = ILLUM_MIRROR_SOUTH
            project_beam(row, col - 1, Direction.WEST, map)
        elif dir == Direction.EAST:
            map_node.illumination = ILLUM_MIRROR_EAST
            project_beam(row - 1, col, Direction.NORTH, map)
    if map_node.element == MapElement.BACKSLASH_MIRROR:
        # Mirror \
        if dir == Direction.NORTH:
            map_node.illumination = ILLUM_MIRROR_NORTH
            project_beam(row, col - 1, Direction.WEST, map)
        elif dir == Direction.WEST:
            map_node.illumination = ILLUM_MIRROR_WEST
            project_beam(row - 1, col, Direction.NORTH, map)
        elif dir == Direction.SOUTH:
            map_node.illumination = ILLUM_MIRROR_SOUTH
            project_beam(row, col + 1, Direction.EAST, map)
        elif dir == Direction.EAST:
            map_node.illumination = ILLUM_MIRROR_EAST
            project_beam(row + 1, col, Direction.SOUTH, map)
    if map_node.element == MapElement.V_SPLITTER:
        # Splitter |
        if dir == Direction.NORTH or dir == Direction.SOUTH:
            map_node.illumination = ILLUM_SPLIT_THROUGH
            project_beam(row + dir.value[0], col, dir, map)
        else:
            map_node.illumination = ILLUM_SPLIT_SPLIT
            # Split the beam
            project_beam(row - 1, col, Direction.NORTH, map)
            project_beam(row + 1, col, Direction.SOUTH, map)
    if map_node.element == MapElement.H_SPLITTER:
        # Splitter -
        if dir == Direction.EAST or dir == Direction.WEST:
            map_node.illumination = ILLUM_SPLIT_THROUGH
            project_beam(row, col + dir.value[1], dir, map)
        else:
            map_node.illumination = ILLUM_SPLIT_SPLIT
            # Split the beam
            project_beam(row, col - 1, Direction.WEST, map)
            project_beam(row, col + 1, Direction.EAST, map)
    
input_data = open("data.txt").read().splitlines()
map_height = len(input_data)
map_width = len(input_data[0])
dark_map = [[None for i in range(map_width)] for j in range(map_height)]
for row_num in range(map_height):
    data_row = input_data[row_num]
    for col_num in range(map_width):
        char = data_row[col_num]
        if char == ".":
            dark_map[row_num][col_num] = MapNode(MapElement.EMPTY, ILLUM_NONE)
        elif char == "/":
            dark_map[row_num][col_num] = MapNode(MapElement.SLASH_MIRROR, ILLUM_NONE)
        elif char == "\\":
            dark_map[row_num][col_num] = MapNode(MapElement.BACKSLASH_MIRROR, ILLUM_NONE)
        elif char == "-":
            dark_map[row_num][col_num] = MapNode(MapElement.H_SPLITTER, ILLUM_NONE)
        elif char == "|":
            dark_map[row_num][col_num] = MapNode(MapElement.V_SPLITTER, ILLUM_NONE)

def copy_map(m: [[MapNode]]) -> [[MapNode]]:
    new_map = []
    for row_num in range(len(m)):
        new_row = []
        for col_num in range(len(m[0])):
            new_node = MapNode(m[row_num][col_num].element, m[row_num][col_num].illumination)
            new_row.append(new_node)
        new_map.append(new_row)
            
    return new_map

def read_map(m: [[MapNode]]) -> int:
    sum = 0
    for row in m:
        for node in row:
            if node.illumination != ILLUM_NONE:
                sum += 1
    return sum

highest_sum = 0
for row_num in range(map_height):
    # Check both sides
    east_map = copy_map(dark_map)
    project_beam(row_num, 0, Direction.EAST, east_map)
    east_illum = read_map(east_map)
    if east_illum > highest_sum:
        highest_sum = east_illum

    west_map = copy_map(dark_map)
    project_beam(row_num, map_width - 1, Direction.WEST, west_map)
    west_illum = read_map(west_map)
    if west_illum > highest_sum:
        highest_sum = west_illum
for col_num in range(map_width):
    # Check top and bottom
    south_map = copy_map(dark_map)
    project_beam(0, col_num, Direction.SOUTH, south_map)
    south_illum = read_map(south_map)
    if south_illum > highest_sum:
        highest_sum = south_illum

    north_map = copy_map(dark_map)
    project_beam(map_height - 1, col_num, Direction.NORTH, north_map)
    north_illum = read_map(north_map)
    if north_illum > highest_sum:
        highest_sum = north_illum


print("Sum: %d" % highest_sum)