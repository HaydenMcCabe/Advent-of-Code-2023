import sys
import re

# Load the data from the file
# into an array.
data_file = open("data.txt")
data_lines = data_file.read().splitlines()
last_line_number = len(data_lines) - 1

number_regex = re.compile("(\d+)")
symbol_regex = re.compile("[^\s\d\.]+")

sum = 0

for line_number in range(len(data_lines)):
    line = data_lines[line_number]
    # Find all instances of numbers in this line
    numbers = number_regex.finditer(line)
    for number in numbers:
        # Track if a symbol has been found near this value
        symbol_found = False

        # Find the range to search for a symbol
        # that is extended by one character in
        # each direction.
        # Note: The end index is the index of the character 
        # AFTER the match and may not be a valid index.
        search_start = max(0, number.span()[0] - 1)
        search_end = min(len(line), number.span()[1]+1)
        # Search the lines above and below for a symbol
        if line_number > 0:
            search_substring = data_lines[line_number-1][search_start:search_end]
            symbol_match = symbol_regex.search(search_substring)
            if symbol_match is not None:
                symbol_found = True
        if line_number < last_line_number:
            search_substring = data_lines[line_number+1][search_start:search_end]
            symbol_match = symbol_regex.search(search_substring)
            if symbol_match is not None:
                symbol_found = True
        # Search the characters before and after the number
        prefix_match = symbol_regex.search(line[search_start])
        if prefix_match is not None:
            symbol_found = True
        suffix_match = symbol_regex.search(line[search_end - 1])
        if suffix_match is not None:
            symbol_found = True
        # If this number corresponds to a symbol, add it to the total
        if symbol_found:
            sum += int(number.group(1))
        
print("Sum: %d" % sum)