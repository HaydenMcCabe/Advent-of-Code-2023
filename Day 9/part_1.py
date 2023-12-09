import re
import functools

def next_value(arr: [int]) -> int:
    # A stack for the last value of each derivative
    last_numbers = []
    current_list = arr
    while True:
        last_numbers.append(current_list[-1])
        derivative_all_zeroes = True
        derivative = []
        for i in range(1,len(current_list)):
            difference = current_list[i] - current_list[i-1]
            derivative.append(difference)
            if difference != 0:
                derivative_all_zeroes = False

        if derivative_all_zeroes:
            return functools.reduce(lambda a, b: a+b, last_numbers)

        # Iterate
        current_list = derivative
        if (len(current_list) == 2):
            return current_list[1] + (current_list[1] - current_list[0]) + functools.reduce(lambda a, b: a+b, last_numbers)

data_lines = open("data.txt").read().splitlines()

sum = 0
line_regex = re.compile("(-?\d+)")
for line in data_lines:
    sequence = list(map(int, line_regex.findall(line)))
    sum += next_value(sequence)

print("Sum: %d" % sum)