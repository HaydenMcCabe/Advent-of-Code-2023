import re
import math

# Parse the two lines of input
input_lines = open("data.txt").read().splitlines()
time_string = re.match(r"Time:(.+)", input_lines[0]).group(1)
distance_string = re.match(r"Distance:(.+)", input_lines[1]).group(1)
times = list(map(float, re.findall(r"(\d+)", time_string)))
distances = list(map(float, re.findall(r"(\d+)", distance_string)))

product = 1

for i in range(len(times)):
    time = times[i]
    distance = distances[i]
    # Solve the quadratic for when the time held would reach the required distance
    root = math.sqrt(time * time - 4 * distance)
    min = math.ceil((time - root)/2)
    max = math.floor((time + root)/2)
    # Exact matches are not allowed
    if min * (time - min) == distance:
        min += 1
    if max * (time - max) == distance:
        max -= 1
    
    product *= max - min + 1

print(product)