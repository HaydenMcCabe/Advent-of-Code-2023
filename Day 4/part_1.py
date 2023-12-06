import re

line_regex = re.compile(r"Card\s+\d+:([\d\s]+)\|([\d\s]+)")
num_regex = re.compile(r"\d+")

input_lines = open("data.txt").read().splitlines()

sum = 0

for line_number in range(len(input_lines)):
    line = input_lines[line_number]
    parts = line_regex.match(line)
    winning_numbers = set(map(int, num_regex.findall(parts.group(1))))
    player_numbers = set(map(int, num_regex.findall(parts.group(2))))
    match_count = len(winning_numbers.intersection(player_numbers))
    if match_count > 0:
        sum += (1 << (match_count - 1))
    
print("Sum: %d" % sum)