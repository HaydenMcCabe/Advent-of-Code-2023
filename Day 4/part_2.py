import re
import functools
import operator

line_regex = re.compile(r"Card\s+\d+:([\d\s]+)\|([\d\s]+)")
num_regex = re.compile(r"\d+")

input_lines = open("data.txt").read().splitlines()

card_counts = [1] * len(input_lines)

sum = 0

for line_number in range(len(input_lines)):
    line = input_lines[line_number]
    parts = line_regex.match(line)
    winning_numbers = set(map(int, num_regex.findall(parts.group(1))))
    player_numbers = set(map(int, num_regex.findall(parts.group(2))))
    match_count = len(winning_numbers.intersection(player_numbers))
    if match_count > 0:
        # Increase the card counts of the following cards
        update_range = range(line_number + 1, line_number + match_count + 1)
        for i in update_range:
            card_counts[i] += card_counts[line_number]
        
print("Sum: %d" % functools.reduce(operator.add, card_counts))