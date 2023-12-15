class rolling_rock:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return "(%d, %d)" % (self.row, self.col)

    def __repr__(self) -> str:
        return self.__str__()
    
    
input_lines = open("data.txt").read().splitlines()
map_height = len(input_lines)
map_width = len(input_lines[0])

# Define functions to move the rocks
def move_north(r: [rolling_rock], m: [[any]]):
    # Sort for lowest row numbers first
    r.sort(key=lambda x: x.row)
    for this_rock in r:
        # Find where this rock would move up to, if it could
        new_row = this_rock.row
        while new_row > 0:
            if map[new_row - 1][this_rock.col] == None:
                new_row -= 1
            else:
                break
        map[this_rock.row][this_rock.col] = None
        map[new_row][this_rock.col] = this_rock
        this_rock.row = new_row

def move_south(r: [rolling_rock], m: [[any]]):
    # Sort for highest row numbers first
    r.sort(key=lambda x: x.row, reverse=True)
    for this_rock in r:
        # Find where this rock would move up to, if it could
        new_row = this_rock.row
        while new_row < len(m) - 1:
            if map[new_row + 1][this_rock.col] == None:
                new_row += 1
            else:
                break
        map[this_rock.row][this_rock.col] = None
        map[new_row][this_rock.col] = this_rock
        this_rock.row = new_row

def move_west(r: [rolling_rock], m: [[any]]):
    # Sort for lowest column number first
    r.sort(key=lambda x: x.col)
    for this_rock in r:
        # Find where this rock would move left to, if it could
        new_col = this_rock.col
        while new_col > 0:
            if map[this_rock.row][new_col - 1] == None:
                new_col -= 1
            else:
                break
        map[this_rock.row][this_rock.col] = None
        map[this_rock.row][new_col] = this_rock
        this_rock.col = new_col        

def move_east(r: [rolling_rock], m: [[any]]):
    # Sort for lowest column number first
    r.sort(key=lambda x: x.col, reverse=True)
    for this_rock in r:
        # Find where this rock would move left to, if it could
        new_col = this_rock.col
        while new_col < len(m[0]) - 1:
            if map[this_rock.row][new_col + 1] == None:
                new_col += 1
            else:
                break
        map[this_rock.row][this_rock.col] = None
        map[this_rock.row][new_col] = this_rock
        this_rock.col = new_col

map = [[None for i in range(map_width)] for j in range(map_height)]
rocks = []
for row_num in range(map_height):
    line = input_lines[row_num]
    for col_num in range(map_width):
        char = line[col_num]
        if char == "O":
            # Create a rolling rock at this location
            new_rock = rolling_rock(row_num, col_num)
            map[row_num][col_num] = new_rock
            rocks.append(new_rock)
        elif char == "#":
            # Put a one at this map location to mark an obstacle.
            map[row_num][col_num] = 1

def print_map(m: [[any]]):
    out_str = ""
    for row_num in range(len(m)):
        line = ""
        for col_num in range(len(m[0])):
            map_element = m[row_num][col_num]
            if map_element == None:
                line += "."
            elif isinstance(map_element, rolling_rock):
                line += "O"
            elif map_element == 1:
                line += "#"
        out_str += line + "\n"
    return out_str

end_positions = {}
cycle_count = 1000000000
for i in range(1000000000):
    move_north(rocks, map)
    move_west(rocks, map)
    move_south(rocks, map)
    move_east(rocks, map)
    after_image = print_map(map)
    if (positions := end_positions.get(after_image, None)) is not None:
        # See if this image will be the same as phase as cycle_count
        period = i - positions[0]
        if (cycle_count - 1 - positions[0]) % period == 0:
            break
        positions.append(i)
    else:
        end_positions[after_image] = [i]

sum = 0
for row_num in range(map_height):
    force = map_height - row_num
    for col_num in range(map_width):
        map_element = map[row_num][col_num]
        if isinstance(map_element, rolling_rock):
            sum += force

print("Sum: %d" % sum)