import sys
import re

# Load the data from the file
# into an array.
data_file = open("data.txt")
data_lines = data_file.read().splitlines()
last_line_number = len(data_lines) - 1

number_regex = re.compile("(\d+)")
symbol_regex = re.compile("\*")

# Make a dictionary to track occurances of the *
# character. The key is a tuple of the line number
# and the character's string index, and the value
# is an array of the values adjacent to it.
gears = {}
# Use a function to update the gears dictionary
# This function takes a line number, a range to search
# in, and the value of the number that called this function.
def track_gears(line_number: int, range: (int, int), number: int):
    substring = data_lines[line_number][range[0]:range[1]]

    matches = symbol_regex.finditer(substring)
    for match in matches:
        key = (line_number, match.span()[0] + range[0])
        # Get any existing values for this key, or [] as a default
        values = gears.get(key, [])
        values.append(number)
        gears[key] = values

for line_number in range(len(data_lines)):
    line = data_lines[line_number]
    # Find all instances of numbers in this line
    numbers = number_regex.finditer(line)
    for number in numbers:
        # Track if a symbol has been found near this value
        symbol_found = False
        int_value = int(number.group(1))
        # Find the range to search for a symbol
        # that is extended by one character in
        # each direction.
        # Note: The end index is the index of the character 
        # AFTER the match and may not be a valid index.
        search_start = max(0, number.span()[0] - 1)
        search_end = min(len(line), number.span()[1]+1)
        # Search the lines above and below
        if line_number > 0:
            track_gears(line_number - 1, (search_start, search_end), int_value)
        if line_number < last_line_number:
            track_gears(line_number + 1, (search_start, search_end), int_value)
        # Search the line where the number was found
        track_gears(line_number, (search_start, search_end), int_value)


sum = 0
for position, values in gears.items():
    if len(values) == 2:
        sum += values[0] * values[1]

print("Sum: %d" % sum)