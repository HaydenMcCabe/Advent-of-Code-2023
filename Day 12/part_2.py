import functools

def arrangements(record: str, vals: [int]) -> int:

    # print("Function begin: %s : %s" % (record, vals))
    # If the elements won't fit, end recursion
    str_length = len(record)
    min_string_length = functools.reduce(lambda x, y: x+y, vals) + len(vals) - 1
    if str_length < min_string_length:
        return 0
    
    str_index = 0
    # Advance the index past any "." characters
    
    while record[str_index] == ".":
        str_index += 1
        if str_index == str_length:
            return 0

    # If the first non-period character is #, make
    # sure the first value will fit
    if record[str_index] == "#":
        str_index += 1
        # The next value - 1 characters
        # must be either # or ?
        for i in range(vals[0] - 1):
            if not (record[str_index + i] == "#" or record[str_index + i] == "?"):
                # The next value won't fit.
                return 0
            
        # Advance to the character after the sequence
        str_index += vals[0] - 1

        # This sequence was the end of the string.
        if str_index == len(record):
            if len(vals) == 1:
                return 1
            else:
                return 0
        
        # The sequence of #s must be followed by . or ?
        if not (record[str_index] == "." or record[str_index] == "?"):
            return 0
        
        # if len(vals) == 1:
            # print("Last val")
            # print("remainder: %s" % record[(str_index + 1):])
        # If this was the last sequence to be fit, and it does, this arrangement works
        # if there are no # characters in the rest of the string
        if len(vals) == 1:
            if "#" in record[(str_index + 1):]:
                return 0
            # print("Tail case: %s" % record[str_index:])
            return 1
        
        # This isn't the end of the string, so increment the index.
        str_index += 1
        # Cut the string after the # sequence
        substring = record[(str_index):]
        # Remove the first element of the array in a new list
        subarray = vals[1:]
        
        # Recur with the remaining string and values
        sub_count = arrangements(substring, subarray)
        return sub_count
    else:
        # The first non-period character is ?
        # Explore the options for both # and ? in this position
        pound_record = "#" + record[(str_index + 1):]
        pound_count = arrangements(pound_record, vals)

        dot_count = arrangements(record[(str_index + 1):], vals)
        return pound_count + dot_count


data_lines = open("data.txt").read().splitlines()
# data_lines = [".???????#?? 4,1"]
# data_lines = ["??????...??## 1,1,4"]
# data_lines = ["??## 4"]
sum = 0
for line in data_lines:
    parts = line.split(" ")
    record = parts[0]
    num_strings = parts[1].split(",")
    nums = list(map(int, num_strings))
    
    # Expand to 5 times the length
    mul_record = ((record + "?") * 5)[0:-1]
    mul_nums = nums * 5


    sum += arrangements(mul_record, mul_nums)

print("Sum: %d" % sum)