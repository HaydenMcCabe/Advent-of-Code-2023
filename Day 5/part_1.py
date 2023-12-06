import re

data = open("data.txt").read()

# Use regex to split the input data into parts
file_parts = re.match(r"seeds:([\d\s]+)seed-to-soil map:([\d\s]+)soil-to-fertilizer map:([\d\s]+)fertilizer-to-water map:([\d\s]+)water-to-light map:([\d\s]+)light-to-temperature map:([\d\s]+)temperature-to-humidity map:([\d\s]+)humidity-to-location map:([\d\s]+)", data)

# Parse the parts collected from the input file

# Make a simple list of seeds
int_regex = re.compile("\d+")
seed_strings = int_regex.findall(file_parts[1])
seeds = list(map(int, seed_strings))

# Compile a reusable regex object for the following
# sections, which all use a three-integers-per-line
# format.
mapping_regex = re.compile("(\d+)\s+(\d+)\s+(\d+)")

def make_map(text: str):
    new_map = []
    # Break the input text into an array of lines
    # and process each individually.
    text_lines = text.splitlines()
    for line in text_lines:
        line_strings = int_regex.findall(line)
        line_values = list(map(int, line_strings))
        if len(line_values) == 3:
            # Make a range of the values that are mapped in this line
            r = range(line_values[1], line_values[1] + line_values[2])
            # Add a line to the map, with the range and its offset
            new_map.append((r, line_values[0]))
            
    return new_map

# Given an input, find its offset value, or if no
# explicit mapping exists, return the original value
def read_map(map, key: int) -> int:
    for (r, offset) in map:
        if key in r:
            return key - r.start + offset
    return key

# Create dictionaries for the lookup tables
seed_to_soil_map = make_map(file_parts[2])
soil_to_fertilizer_map = make_map(file_parts[3])
fertilizer_to_water_map = make_map(file_parts[4])
water_to_light_map = make_map(file_parts[5])
light_to_temperature_map = make_map(file_parts[6])
temperature_to_humidity_map = make_map(file_parts[7])
humidity_to_location_map = make_map(file_parts[8])

# Given a seed number, find the location by searching all of the maps
def find_location(seed: int) -> int:
    soil = read_map(seed_to_soil_map, seed)
    fertilizer = read_map(soil_to_fertilizer_map, soil)
    water = read_map(fertilizer_to_water_map, fertilizer)
    light = read_map(water_to_light_map, water)
    temperature = read_map(light_to_temperature_map, light)
    humidity = read_map(temperature_to_humidity_map, temperature)
    location = read_map(humidity_to_location_map, humidity)
    return location

# Map all of the seeds to locations
locations = list(map(find_location, seeds))
locations.sort()
print("Lowest location number: %d" % locations[0])