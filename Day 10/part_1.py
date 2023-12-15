import re
import sys
import functools

sys.setrecursionlimit(1_000_000)

output_file = open("output.txt", "w")

# A recursive function to find a closed loop ending at "S", and returns an array of the positions
# in the loop
def loop_length(position: (int, int), origin: (int, int), map: [str], distance: int) -> int:
    this_char = map[position[0]][position[1]]
    
    if this_char == "S":
        return distance
    
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

    return loop_length(next_position, position, map, distance + 1)



map = open('data.txt').read().splitlines()
for row in range(len(map)):
    if (match := re.search("S", map[row])) is not None:
        col = match.span()[0]
        position = (row, col)
        if row > 0:
            above = (row - 1, col)
            above_char = map[row - 1][col]
            if above_char == "|" or above_char == "F" or above_char == "7":
                length = loop_length(above, position, map, 1)
                if length != -1:
                    print("Length: %d" % (length >> 1))
                    break
        if row < len(map) - 1:
            below = (position[0] + 1, position[1])
            below_char = map[position[0] + 1][position[1]]
            if below_char == "|" or below_char == "L" or below_char == "J":
                length = loop_length(below, position, map, 1)
                if length != -1:
                    print("Length: %d" % (length >> 1))
                    break
        if col > 0:
            left = (position[0], position[1] - 1)
            left_char = map[position[0]][position[1] - 1]
            if left_char == "-" or left_char == "L" or left_char == "F":
                length = loop_length(left, position, map, 1)
                if length != -1:
                    print("Length: %d" % (length >> 1))
                    break
        if col < len(map[row]) - 1:
            right = (position[0], position[1] + 1)
            right_char = map[position[0]][position[1] + 1]
            if right_char == "-" or right_char == "J" or right_char == "7":
                length = loop_length(right, position, map, 1)
                if length != -1:
                    print("Length: %d" % (length >> 1))
                    break
        break
