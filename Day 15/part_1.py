def dumb_hash(s: str):
    ascii_values = list(s.encode("ascii"))
    hash_val = 0
    for val in ascii_values:
        hash_val += val
        hash_val *= 17
        hash_val &= 0xff
    return hash_val

input = open("data.txt").read().split(",")
sum = 0
for command in input:
    sum += dumb_hash(command)

print("Sum: %d" % sum)