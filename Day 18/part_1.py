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

# The corner shapes, based on the previous and
# current directions.
corners = {
    "U": {"L": "7", "R": "F"},
    "D": {"L": "J", "R": "L"},
    "L": {"U": "L", "D": "F"},
    "R": {"U": "J", "D": "7"}
}
lines = {
    "U": "|",
    "D": "|",
    "L": "-",
    "R": "-"
}

line_regex = re.compile(r"([UDLR]) (\d+) \(#([0-9a-f]+)\)")
data_lines = open("data.txt").read().splitlines()

# Track the previous direction to compute corners
# Use the last entry to choose a starting direction
previous_direction = line_regex.match(data_lines[-1]).group(1)

for data_row in data_lines:
    parts = line_regex.match(data_row).group
    direction = parts(1)
    # Update the position to use the correct corner
    edges[(pos_x, pos_y)] = corners[previous_direction][direction]


    for _ in range(int(parts(2))):
        # Get values from the lookup tables.
        pos_x += delta[parts(1)][0]
        pos_y += delta[parts(1)][1]
        
        min_x = min(pos_x, min_x)
        min_y = min(pos_y, min_y)
        max_x = max(pos_x, max_x)
        max_y = max(pos_y, max_y)

        if pos_x != 0 or pos_y != 0:
            edges[(pos_x, pos_y)] = lines[direction]

    previous_direction = direction
        
# Algorithm to find locations inside a loop copied and modified
# from Day 10
    
sum = len(edges)
col_count = max_x - min_x + 1
for y in range(min_y, max_y + 1):
    x = min_x
    pipe_mod = 0
    while x <= max_x:
        if (piece_at_location := edges.get((x, y), None)) is not None:
            # There is a piece of the loop at (row, col)
            if piece_at_location == "|":
                pipe_mod = (pipe_mod + 1) % 2
                x += 1
            elif piece_at_location == "F" or piece_at_location == "L":
                # Advance past any - pieces
                x += 1
                while edges[(x, y)] == "-":
                    x += 1
                end_piece = edges[(x, y)]
                if end_piece == "7" and piece_at_location == "L":
                    pipe_mod = (pipe_mod + 1) % 2
                elif end_piece == "J" and piece_at_location == "F":
                    pipe_mod = (pipe_mod + 1) % 2
                x += 1
            else:
                print("Bad parsing")
                sys.exit()
            
        else:
            # This location is not a piece of the loop
            sum += pipe_mod
            x += 1

print("Sum: %d" % sum)
