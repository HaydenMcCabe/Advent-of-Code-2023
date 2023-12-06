import re
import math

# Parse the two lines of input
input_lines = open("data.txt").read().splitlines()
time_string = re.match(r"Time:(.+)", input_lines[0]).group(1)
distance_string = re.match(r"Distance:(.+)", input_lines[1]).group(1)
# Remove whitespace from the strings
time = float(re.sub(r"\s", "", time_string))
distance = float(re.sub(r"\s", "", distance_string))

# Solve the quadratic for when the time held would reach the required distance
root = math.sqrt(time * time - 4 * distance)
min = math.ceil((time - root)/2)
max = math.floor((time + root)/2)
# Exact matches are not allowed
if min * (time - min) == distance:
    min += 1
if max * (time - max) == distance:
    max -= 1

winners = max - min + 1
print(winners)