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

move_north(rocks, map)

sum = 0
for row_num in range(map_height):
    force = map_height - row_num
    for col_num in range(map_width):
        map_element = map[row_num][col_num]
        if isinstance(map_element, rolling_rock):
            sum += force

print("Sum: %d" % sum)