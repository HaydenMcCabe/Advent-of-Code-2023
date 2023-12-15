import re
import sys
import functools

sys.setrecursionlimit(1_000_000)

output_file = open("output.txt", "w")

# A recursive function to find a closed loop ending at "S", and returns an array of the positions
# in the loop
def loop_length(position: (int, int), origin: (int, int), map: [str], distance: int) -> [((int, int), int)]:
    this_char = map[position[0]][position[1]]
    if this_char == "S":
        return [(position, 0)]
    
    # Positions around here
    left = (position[0], position[1] - 1)
    right = (position[0], position[1] + 1)
    above = (position[0] - 1, position[1])
    below = (position[0] + 1, position[1])

    if this_char == "|":
        paths = set([above, below])
        pipemask = 2
    elif this_char == "-":
        paths = set([left, right])
        pipemask = 1
    elif this_char == "L":
        paths = set([above, right])
        pipemask = 3
    elif this_char == "J":
        paths = set([above, left])
        pipemask = 3
    elif this_char == "F":
        paths = set([below, right])
        pipemask = 3
    elif this_char == "7":
        paths = set([below, left])
        pipemask = 3

    paths.remove(origin)
    next_position = paths.pop()

    
    return loop_length(next_position, position, map, distance + 1) + [(position, pipemask)]
 



map = open('test_data.txt').read().splitlines()
for row in range(len(map)):
    if (match := re.search("S", map[row])) is not None:
        col = match.span()[0]
        position = (row, col)

        above = (row - 1, col)
        below = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        if row > 0:
            above_char = map[row - 1][col]
            if above_char == "|" or above_char == "F" or above_char == "7":
                loop = loop_length(above, position, map, 1)
                break
        if row < len(map) - 1:
            below_char = map[position[0] + 1][position[1]]
            if below_char == "|" or below_char == "L" or below_char == "J":
                loop = loop_length(below, position, map, 1)
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

# Replace the first element in our loop, corresponding to "S", with its equivalent 
# using the correct pipe.
s_mask = 0
adjacent = [loop[1][0], loop[-1][0]]
for pipe in adjacent:
    if pipe == left or pipe == right:
        s_mask |= 2
    if pipe == above or pipe == below:
        s_mask |= 1
loop[0] = (loop[0][0], s_mask)

# Build a hash table of the results
pipe_hash = {}
for pipe in loop:
    pipe_hash[pipe[0]] = pipe[1]

sum = 0
for row_num in range(len(map)):
    row = map[row_num]
    left_pipe_count = 0
    for col in range(len(row)):
        if pipe_hash.get((row_num, col), None) is None:
            if left_pipe_count & 1 == 1:
                sum += 1
                print("LEFT case: (%d, %d)" % (row_num, col))
        else:
            left_pipe_count += 1
