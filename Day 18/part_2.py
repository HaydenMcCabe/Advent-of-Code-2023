import re
import sys
# Track the current position
pos_x = 0
pos_y = 0
# Create a list with the positions of the trench,
# and a symbol to represent straight sections and corners
# a la day 10.
edges = {}
min_x = 0
max_x = 0
min_y = 0
max_y = 0

# Make a lookup table for movement vectors.
delta = {
    "U": (0,1),
    "D": (0,-1),
    "L": (-1,0),
    "R": (1,0)
}

line_regex = re.compile(r"#([0-9a-f]{5})([0123])")
def decode_hex(hex_string: str) -> (str, int):
    matches = line_regex.search(hex_string)
    distance = int(matches.group(1), 16)
    if matches.group(2) == "0":
        return ("R", distance)
    if matches.group(2) == "1":
        return ("D", distance)
    if matches.group(2) == "2":
        return ("L", distance)
    if matches.group(2) == "3":
        return ("U", distance)

# Track the previous direction to compute corners
corners =[]
data_lines = open("test_data.txt").read().splitlines()
for data_row in data_lines:
    parts = decode_hex(data_row)
    direction = parts[0]

    pos_x += delta[parts[0]][0] * parts[1]
    pos_y += delta[parts[0]][1] * parts[1]

    corners.append((pos_x, pos_y))
corners.sort()

class internal_area:
    left: int
    bottom: int
    top: int
    
    def __init__(self, left:int , bottom: int, top:int ) -> None:
        self.left = left
        self.bottom = bottom
        self.top = top
        
    def __lt__(self, other):
        return self.bottom < other.bottom

i = 0
open_areas: [internal_area] = []

while i < len(corners):
    x = corners[i][0]
    lines = []
    while i < len(corners) and corners[i][0] == x:
        lines.append((corners[i][1], corners[i+1][1]))
        i += 2
    if len(open_areas) == 0:
        # Initial state: Create an area for each line
        for line in lines:
            new_area = internal_area(x, line[0], line[1])
            open_areas.append(new_area)
    else:
        area_index = 0
        line_index = 0
        # Handle each line
        while line_index < len(lines):
            line = lines[line_index]
            # A line entirely below open areas is the left side
            # of a new area.
            if line[1] < open_areas[area_index].bottom:
                new_area = internal_area(x, line[0], line[1])
                open_areas.append(new_area)

            line_index += 1

    open_areas.sort()