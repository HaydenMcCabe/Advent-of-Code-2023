import sys

# Load the data from the file
# into an array.
data_file = open("data.txt")
data_lines = data_file.read().splitlines()

sum = 0
for line_number in range(len(data_lines)):
    line = data_lines[line_number]
    first = -1
    last = -1
    for i in range(len(line)):
        # See if this character is a digit
        if line[i].isdigit():
            digit = int(line[i])
            if first == -1:
                first = digit
            last = digit
    
    # Verify the input data was good
    if first == -1 or last == -1:
        print("Unable to parse input data from line %d: %s\n" % (line_number, line))
        sys.exit()

    # Convert the digits found in this line into a 2 digit number
    value = first * 10 + last
    sum += value

# Output the total
print(sum)