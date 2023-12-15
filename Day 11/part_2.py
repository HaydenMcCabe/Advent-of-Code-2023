data_rows = open("data.txt").read().splitlines()

blank_cols = []
for col in range(len(data_rows[0])):
    col_blank = True
    for row in range(len(data_rows)):
        if data_rows[row][col] != ".":
            col_blank = False
            break
    if col_blank:
        blank_cols.append(col)
    
expanded_rows = 0
galaxies = []
for row_num in range(len(data_rows)):
    row = data_rows[row_num]
    row_blank = True
    expanded_col = 0
    for col_num in range(len(row)):
        if row[col_num] == "#":
            row_blank = False
            galaxies.append((row_num + (expanded_rows * (1000000 - 1)), expanded_col))
        if col_num in blank_cols:
            expanded_col += 1000000
        else:
            expanded_col += 1
    if row_blank:
        expanded_rows += 1
    
distances = []
sum = 0
for start in range(len(galaxies)):
    start_galaxy = galaxies[start]
    for end in range(start + 1, len(galaxies)):
        end_galaxy = galaxies[end]
        dx = abs(end_galaxy[1] - start_galaxy[1])
        dy = abs(end_galaxy[0] - start_galaxy[0])
        sum += dx + dy

print(sum)