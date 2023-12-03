import sys

# Load the data from the file
# into an array.
data_file = open("data.txt")
data_lines = data_file.read().splitlines()

# Define an array of numerals and their
# string equivalents
digit_strings = [
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9)
]

sum = 0
for line_number in range(len(data_lines)):
    line = data_lines[line_number].lower()
    first = -1
    last = -1
    # Check this position for a value.
    for str_index in range(len(line)):
        # See if this character is a digit.
        if line[str_index].isdigit():
            digit = int(line[str_index])
            if first == -1:
                first = digit
            last = digit
        # See if this character is the start
        # of the textual description of a digit.
        else:
            for digit_string in digit_strings:
                if line.startswith(digit_string[0], str_index):
                    if first == -1:
                        first = digit_string[1]
                    last = digit_string[1]
            

    # Verify the input data was good
    if first == -1 or last == -1:
        print("Unable to parse input data from line %d: %s\n" % (line_number, line))
        sys.exit()

    # Convert the digits found in this line into a 2 digit number
    value = first * 10 + last
    sum += value

# Output the total
print(sum)