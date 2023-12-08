import re
import math

data_lines = open("data.txt").read().splitlines()

# Regexes
directions_regex = re.compile("[LR]")
map_regex = re.compile("(\w+)\s+=\s+\((\w+),\s+(\w+)\)")

directions = directions_regex.findall(data_lines[0])
map = {}
loop_lengths = []
travel_to_z = []

locations = []
for line_number in range(2, len(data_lines)):
    map_parts = map_regex.match(data_lines[line_number])
    if map_parts[1][2] == "A":
        locations.append(map_parts[1])
    map[map_parts[1]] = (map_parts[2], map_parts[3])


for start in locations:
    direction_index = 0
    current_location = start
    steps = 0
    direction_count = len(directions)
    log = {}
    z_steps = []

    while True:
        # Record at which step counts the location ends in Z
        if current_location[2] == "Z":
            z_steps.append(steps)
        
        # For this location, record direction_index/steps
        location_log: {int:int} = log.get(current_location, None)
        if location_log is not None:
            # The key is the current direction_index,
            # and the value is the current step count.
            # See if we've been here before at this direction_index
            if direction_index in location_log:
                previous_steps = location_log[direction_index]
                loop_lengths.append(steps - previous_steps)
                travel_to_z.append(z_steps)
                break
            else:
                location_log[direction_index] = steps
        else:
            log[current_location] = {direction_index:steps}
        
        move_direction = directions[direction_index]
        move_locations = map[current_location]
        next_location = move_locations[0 if move_direction == "L" else 1]

        current_location = next_location
        steps += 1
        direction_index += 1
        if direction_index == direction_count:
            direction_index = 0
        
total_steps = math.lcm(*loop_lengths)
print("Total steps: %d" % total_steps)