import sys
import re

red_max = 12
green_max = 13
blue_max = 14

sum = 0

# Load the data from the file
# into an array.
data_file = open("data.txt")
data_lines = data_file.read().splitlines()

for line_number in range(len(data_lines)):
    line = data_lines[line_number]

    # Split the line at the colon, and ensure there is only one
    line_parts = line.split(":")
    if len(line_parts) != 2:
        sys.exit()

    red_seen = 0
    green_seen = 0
    blue_seen = 0

    # Check each measurement for an invalid value
    samples = line_parts[1].split(";")
    for sample in samples:
        red = re.search("(\d+) red", sample)
        if red is not None:
            red_count = int(red.group(1))
            if red_count > red_seen:
                red_seen = red_count

        green = re.search("(\d+) green", sample)
        if green is not None:
            green_count = int(green.group(1))
            if green_count > green_seen:
                green_seen = green_count

        blue = re.search("(\d+) blue", sample)
        if blue is not None:
            blue_count = int(blue.group(1))
            if blue_count > blue_seen:
                blue_seen = blue_count
        
    game_search = re.search("Game (\d+)", line_parts[0])
    if game_search is None:
        print("Unable to parse game number.")
        sys.exit()

    sum += red_seen * green_seen * blue_seen

print(sum)