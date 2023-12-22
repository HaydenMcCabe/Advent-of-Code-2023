from queue import PriorityQueue
data_lines = open("data.txt").read().splitlines()

map_height = len(data_lines)
map_width = len(data_lines[0])

# A 2-dimensional array of booleans to mark visited locations
scheduled = [[False for i in range(map_width)] for j in range(map_height)]
steps = 64
locations = [0]

start_location = (-1,-1)
queue = PriorityQueue()
# Mark any locations that are inaccesable as being scheduled
# so the algorithm will ignore them.
for row_num in range(map_height):
    row = data_lines[row_num]
    for col_num in range(map_width):
        if row[col_num] == "#":
            scheduled[row_num][col_num] = True
        if row[col_num] == "S":
            start_location = (row_num, col_num)

def travel(distance: int, row: int, col: int):
    # Evenly numbered distances are accessable
    if distance & 1 == 0:
        locations[0] += 1
    # End recursion if the total distance is traveled
    # or this location has been visited on this path
    if distance == 0:
        return

    priority = steps - distance + 1
    # Recur for every possible direction
    if row > 0 and not scheduled[row-1][col]:
        queue.put((priority, (distance-1, row-1, col)))
        scheduled[row-1][col] = True
    if row < map_height - 1 and not scheduled[row+1][col]:
        queue.put((priority, (distance-1, row+1, col)))
        scheduled[row+1][col] = True
    if col > 0 and not scheduled[row][col-1]:
        queue.put((priority, (distance-1, row, col-1)))
        scheduled[row][col-1] = True
    if col < map_width - 1 and not scheduled[row][col+1]:
        queue.put((priority, (distance-1, row, col+1)))
        scheduled[row][col+1] = True

scheduled[start_location[0]][start_location[1]] = True
queue.put((0, (steps, start_location[0], start_location[1])))

while not queue.empty():
    _, next = queue.get()
    travel(next[0], next[1], next[2])

print("Locations: %d" % locations[0])