import re
import functools

def previous_value(arr: [int]) -> int:
    # A stack for the last value of each derivative
    first_numbers = []
    current_list = arr
    while True:
        first_numbers.append(current_list[0])
        derivative_all_zeroes = True
        derivative = []
        for i in range(1,len(current_list)):
            difference = current_list[i] - current_list[i-1]
            derivative.append(difference)
            if difference != 0:
                derivative_all_zeroes = False

        if derivative_all_zeroes:
            val = 0
            while len(first_numbers) > 0:
                val = first_numbers.pop() - val
            return val

        # Iterate
        current_list = derivative
        if (len(current_list) == 1):
            val = current_list[0]
            while len(first_numbers) > 0:
                val = first_numbers.pop() - val
            return val

data_lines = open("data.txt").read().splitlines()

sum = 0
line_regex = re.compile("(-?\d+)")
for line in data_lines:
    sequence = list(map(int, line_regex.findall(line)))
    sum += previous_value(sequence)

print("Sum: %d" % sum)