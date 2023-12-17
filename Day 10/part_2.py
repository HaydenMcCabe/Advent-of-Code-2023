import re
import sys
import functools

sys.setrecursionlimit(1_000_000)

# A recursive function to find a closed loop ending at "S", and returns an array of the positions
# in the loop
def loop_length(position: (int, int), origin: (int, int), map: [str], distance: int) -> [((int, int), str)]:
    this_char = map[position[0]][position[1]]
    if this_char == "S":
        return [(position, "S")]
    
    # Positions around here
    left = (position[0], position[1] - 1)
    right = (position[0], position[1] + 1)
    above = (position[0] - 1, position[1])
    below = (position[0] + 1, position[1])

    if this_char == "|":
        paths = set([above, below])
    elif this_char == "-":
        paths = set([left, right])
    elif this_char == "L":
        paths = set([above, right])
    elif this_char == "J":
        paths = set([above, left])
    elif this_char == "F":
        paths = set([below, right])
    elif this_char == "7":
        paths = set([below, left])

    paths.remove(origin)
    next_position = paths.pop()
    
    return loop_length(next_position, position, map, distance + 1) + [(position, this_char)]
 
map = open('data.txt').read().splitlines()
for row in range(len(map)):
    if (match := re.search("S", map[row])) is not None:
        col = match.span()[0]
        position = (row, col)

        above = (row - 1, col)
        left = (row, col - 1)
        right = (row, col + 1)
        below = (row + 1, col)

        if row > 0:
            above_char = map[row - 1][col]
            if above_char == "|" or above_char == "F" or above_char == "7":
                loop = loop_length(above, position, map, 1)
                break
        if col > 0:
            left_char = map[position[0]][position[1] - 1]
            if left_char == "-" or left_char == "L" or left_char == "F":
                loop = loop_length(left, position, map, 1)
                break
        if col < len(map[row]) - 1:
            right_char = map[position[0]][position[1] + 1]
            if right_char == "-" or right_char == "J" or right_char == "7":
                loop = loop_length(right, position, map, 1)
                break    
        break

# Replace the S at the first position of the loop with
# the appropriate pipe
first_pos = loop[-1][0]
last_pos = loop[1][0]
# If the difference in the row of first and last is 2, the piece is |
if abs(first_pos[0] - last_pos[0]) == 2:
    loop[0] = (loop[0][0], "|")
# If the difference in the col of first and last is 2, the piece is -
elif abs(first_pos[1] - last_pos[1]) == 2:
    loop[0] = (loop[0][0], "-")
# Check for elbow pieces
elif first_pos == above:
    if last_pos == left:
        loop[0] = (loop[0][0], "J")
    elif last_pos == right:
        loop[0] = (loop[0][0], "L")
elif first_pos == left:
    if last_pos == above:
        loop[0] = (loop[0][0], "J")
    elif last_pos == below:
        loop[0] = (loop[0][0], "7")
elif first_pos == right:
    if last_pos == above:
        loop[0] = (loop[0][0], "L")
    elif last_pos == below:
        loop[0] = (loop[0][0], "F")

# Create a hash table for the loop pieces
pipe_hash = {}
for piece in loop:
    pipe_hash[piece[0]] = piece[1]

# Now with all of the loop data, we can look
# at the spaces that are inside of it.
# The first row can be skipped, as it's impossible
# for anything to be inside the loop.
sum = 0
col_count = len(map[0])
for row in range(1, len(map)):
    col = 0
    pipe_mod = 0
    while col < col_count:
        if (piece_at_location := pipe_hash.get((row, col), None)) is not None:
            # There is a piece of the loop at (row, col)
            if piece_at_location == "|":
                pipe_mod = (pipe_mod + 1) % 2
                col += 1
            elif piece_at_location == "F" or piece_at_location == "L":
                # Advance past any - pieces
                col += 1
                while pipe_hash[(row, col)] == "-":
                    col += 1
                end_piece = pipe_hash[(row, col)]
                if end_piece == "7" and piece_at_location == "L":
                    pipe_mod = (pipe_mod + 1) % 2
                elif end_piece == "J" and piece_at_location == "F":
                    pipe_mod = (pipe_mod + 1) % 2
                col += 1
            else:
                print("Bad parsing")
                sys.exit()
            
        else:
            # This location is not a piece of the loop
            sum += pipe_mod
            col += 1

print("Sum: %d" % sum)