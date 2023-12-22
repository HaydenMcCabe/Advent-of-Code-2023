blocks = open("data.txt").read().split("\n\n")

def string_to_int(s: str) -> int:
    val = 0
    for char_index in range(len(s)):
        if s[char_index] == "#":
            val |= 1
        val = val << 1
    return val >> 1

def single_bit_pos(v: int) -> any:
    one_bit_mask = 1
    shifts = 0
    while one_bit_mask <= v:
        if one_bit_mask == v:
            return shifts
        one_bit_mask = one_bit_mask << 1
        shifts += 1
    return None

def append_bits(s: str, vals: [int]):
    for i in range(len(vals)):
        if s[i] == "#":
            vals[i] = (vals[i] << 1) | 1
        else:
            vals[i] = vals[i] << 1

def has_v_symmetry(v_ints: [int], start_col: int, end_col: int) -> bool:
    left = ((end_col - start_col) >> 1) + start_col
    right = left + 1
    bitmask = 0
    while right <= end_col:
        bitmask ^= v_ints[left]
        bitmask ^= v_ints[right]
        if bitmask > 0 and single_bit_pos(bitmask) is None:
            return False
        left -= 1
        right += 1
    return True

def has_h_symmetry(lines: [str], start_row: int, end_row: int) -> bool:
    top = ((end_row - start_row) >> 1) + start_row
    bottom = top + 1
    bitmask = 0
    
    while bottom <= end_row:
        bitmask ^= string_to_int(lines[top])
        bitmask ^= string_to_int(lines[bottom])
        if bitmask > 0 and single_bit_pos(bitmask) is None:
            return False
        top -= 1
        bottom += 1
    return True

sum = 0
for block in blocks:
    lines = block.splitlines()
    # Create an array of ints representing the columns
    v_ints =[0] * len(lines[0])
    append_bits(lines[0], v_ints)
    
    # Iterate through the lines after the first
    # checking for horizontal symmetries and updating
    # the column ints when checking top to bottom.
    inner_break = False
    sym_mask = string_to_int(lines[0])
    # Check top to bottom
    for line_index in range(1, len(lines)):
        sym_mask ^= string_to_int(lines[line_index])
        if (pos := single_bit_pos(sym_mask)) is not None:
            if has_h_symmetry(lines, 0, line_index):
                rows_above = (line_index >> 1) + 1
                sum += 100 * rows_above
                inner_break = True
                break
        append_bits(lines[line_index], v_ints)
    if inner_break:
        continue

    # Check bottom to top
    sym_mask = string_to_int(lines[-1])
    for line_index in reversed(range(len(lines) - 1)):
        sym_mask ^= string_to_int(lines[line_index])
        if (pos := single_bit_pos(sym_mask)) is not None:
            if has_h_symmetry(lines, line_index, len(lines) - 1):
                rows_below = ((len(lines) - line_index) >> 1)
                rows_above = len(lines) - rows_below
                sum += 100 * rows_above
                inner_break = True
                break
    if inner_break:
        continue

    # Check left to right
    sym_mask = v_ints[0]
    for col_index in range(1, len(v_ints)):
        sym_mask ^= v_ints[col_index]
        if (pos := single_bit_pos(sym_mask)) is not None:
            if has_v_symmetry(v_ints, 0, col_index):
                rows_to_left = (col_index >> 1) + 1
                header = ("-" * (rows_to_left - 1)) + "vv"
                sum += rows_to_left
                inner_break = True
                break
    if inner_break:
        continue    

    # Check right to left
    sym_mask = v_ints[-1]
    for col_index in reversed(range(len(v_ints) - 1)):
        sym_mask ^= v_ints[col_index]
        if (pos := single_bit_pos(sym_mask)) is not None:
            rows_to_right = ((len(v_ints) - col_index) >> 1)
            rows_to_left = (len(v_ints) - rows_to_right)
            if has_v_symmetry(v_ints, col_index, len(v_ints) - 1):
                header = ("-" * (rows_to_left - 1)) + "vv"
                sum += rows_to_left
                inner_break = True
                break
    if inner_break:
        continue


print("Sum: %d" % sum)