# Return true if the line is symmetric about a line after an index
def symmetry_filter(line: str, index: int) -> bool:
    d = 0
    symmetric = True
    while (index - d >= 0) and (index + d + 1 < len(line)):
        if line[index - d] != line[index + d + 1]:
            symmetric = False
            break
        d += 1
    return symmetric

blocks = open("data.txt").read().split("\n\n")
sum = 0
for block in blocks:
    lines = block.splitlines()
    # Look for possible symmetries in the first line
    v_symmetries = []
    first_line = lines[0]
    last_char = len(first_line) - 1
    for i in range(len(first_line) - 1):
        symmetric = False
        if first_line[i] == first_line[i+1]:
            symmetric = True
            d = 1
            while (i - d >= 0) and (i + d + 1 <= last_char):
                if first_line[i - d] != first_line[i + d + 1]:
                    symmetric = False
                    break
                d += 1
        if symmetric:
            v_symmetries.append(i)

    # Check the remaining lines, to see if the potential vertical
    # symmetries apply, and if the line is the first in the
    # lower half of a horizontal symmetry.
    h_symmetry = -1
    for i in range(1, len(lines)):
        line = lines[i]
        # Filter the symmetries based on this line, removing
        # any indecies that won't work based on this line.
        v_symmetries = list(filter(lambda val: symmetry_filter(line, val), v_symmetries))

        # Check to see if the lines starting here and below match
        # lines above this line
        h_start = i - 1
        h_end = i
        h_symmetric = True
        while (h_start >= 0) and (h_end < len(lines)):
            if lines[h_start] != lines[h_end]:
                h_symmetric = False
                break
            h_start -= 1
            h_end += 1
        if h_symmetric:
            h_symmetry = i

    if len(v_symmetries) == 1:
        sum += v_symmetries[0] + 1
    if h_symmetry != -1:
        sum += 100 * h_symmetry

print("Sum: %d" % sum)