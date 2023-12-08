import re

data_lines = open("data.txt").read().splitlines()

# Regexes
directions_regex = re.compile("[LR]")
map_regex = re.compile("(\w+)\s+=\s+\((\w+),\s+(\w+)\)")

directions = directions_regex.findall(data_lines[0])
map = {}
for line_number in range(2, len(data_lines)):
    map_parts = map_regex.match(data_lines[line_number])
    map[map_parts[1]] = (map_parts[2], map_parts[3])

direction_index = 0
steps = 0
location = 'AAA'
while True:
    paths = map[location]
    next_direction = directions[direction_index]
    location = paths[0 if next_direction == "L" else 1]
    steps += 1
    direction_index += 1
    if direction_index == len(directions):
        direction_index = 0
    if location == 'ZZZ':
        break

print("Steps: %d" % steps)