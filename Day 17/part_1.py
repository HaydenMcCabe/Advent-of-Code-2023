from queue import PriorityQueue
from enum import Enum

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

class BlockNode():
    cost: int
    location: (int, int)
    direction: Direction

    def __init__(self, cost: int, location: (int, int), direction: Direction) -> None:
        self.cost = cost
        self.location = location
        self.direction = direction

# Return the taxicab distance from the position to the goal
def heuristic(location: (int, int), goal: (int, int)) -> int:
    return (goal[0] - location[0]) + (goal[1] - location[1])


# Convert the input text into an array of integers
data = open("test_data.txt").read().splitlines()
map = []
for row_num in range(len(data)):
    int_line = []
    row = data[row_num]
    for col_num in range(len(row)):
        int_line.append(int(row[col_num]))
    map.append(int_line)
map_height = len(map)
map_width = len(map[0])

# The goal node is the bottom right corner
goal = (len(map) - 1, len(map[0]) - 1)

# Make a priority queue to implement A*
open_queue = PriorityQueue()
# At the beginning is the only time the options aren't
# on a straight line, so add them manually.
e1 = BlockNode(map[0][1], (0,1), Direction.EAST)
e2 = BlockNode(map[0][1] + map[0][2], (0,2), Direction.EAST)
e3 = BlockNode(map[0][1] + map[0][2] + map[0][3], (0,3), Direction.EAST)

s1 = BlockNode(map[1][0], (1,0), Direction.SOUTH)
s2 = BlockNode(map[1][0] + map[2][0], (2,0), Direction.SOUTH)
s3 = BlockNode(map[1][0] + map[2][0] + map[3][0], (3,0), Direction.SOUTH)

open_queue.put((heuristic(e1.location, goal) + e1.cost, e1))
open_queue.put((heuristic(e2.location, goal) + e2.cost, e2))
open_queue.put((heuristic(e3.location, goal) + e3.cost, e3))
open_queue.put((heuristic(s1.location, goal) + s1.cost, s1))
open_queue.put((heuristic(s2.location, goal) + s2.cost, s2))
open_queue.put((heuristic(s3.location, goal) + s3.cost, s3))

while not open_queue.empty():
    node: BlockNode    
    _, node = open_queue.get()
    node_row = node.location[0]
    node_col = node.location[1]

    
    # The lowest cost path has been found if the
    # goal node is the highest priority.
    if node.location == goal:
        print("Cost: %d", node.cost)
        break

    print("Checking from location (%d, %d)" % node.location)

    # There are as many as six nodes that can be reached
    # from the current node
    if node.direction == Direction.EAST or node.direction == Direction.WEST:
        # Northbound nodes
        if node_row > 0:
            n1_cost = node.cost + map[node_row - 1][node_col]
            h = heuristic((node_row - 1, node_col), goal)
            open_queue.put((n1_cost + h, \
                BlockNode(n1_cost, (node_row - 1, node_col), \
                Direction.NORTH)))
        if node_row > 1:
            n2_cost = n1_cost + map[node_row - 2][node_col]
            h = heuristic((node_row - 2, node_col), goal)
            open_queue.put((n2_cost + h, \
                BlockNode(n2_cost, (node_row - 2, node_col), \
                Direction.NORTH)))
        if node_row > 2:
            n3_cost = n2_cost + map[node_row - 3][node_col]
            h = heuristic((node_row - 3, node_col), goal)
            open_queue.put((n1_cost + h, \
                BlockNode(n3_cost, (node_row - 3, node_col), \
                Direction.NORTH)))
        # Southbound nodes
        if node_row < map_height - 1:
            s1_cost = node.cost + map[node_row + 1][node_col]
            h = heuristic((node_row + 1, node_col), goal)
            open_queue.put((s1_cost + h, \
                BlockNode(s1_cost, (node_row + 1, node_col), \
                Direction.SOUTH)))
        if node_row < map_height - 2:
            s2_cost = s1_cost + map[node_row + 2][node_col]
            h = heuristic((node_row + 2, node_col), goal)
            open_queue.put((s2_cost + h, \
                BlockNode(s2_cost, (node_row + 2, node_col), \
                Direction.SOUTH)))
        if node_row < map_height - 3:
            s3_cost = s2_cost + map[node_row + 3][node_col]
            h = heuristic((node_row + 3, node_col), goal)
            open_queue.put((s1_cost + h, \
                BlockNode(s3_cost, (node_row + 3, node_col), \
                Direction.SOUTH)))
    else:
         # Westbound nodes
        if node_col > 0:
            w1_cost = node.cost + map[node_row][node_col - 1]
            h = heuristic((node_row, node_col - 1), goal)
            open_queue.put((w1_cost + h, \
                BlockNode(w1_cost, (node_row, node_col - 1), \
                Direction.WEST)))
        if node_col > 1:
            w2_cost = w1_cost + map[node_row][node_col - 2]
            h = heuristic((node_row, node_col - 2), goal)
            open_queue.put((w2_cost + h, \
                BlockNode(w2_cost, (node_row, node_col - 2), \
                Direction.WEST)))
        if node_col > 2:
            w3_cost = w2_cost + map[node_row][node_col - 3]
            h = heuristic((node_row, node_col - 3), goal)
            open_queue.put((w3_cost + h, \
                BlockNode(w3_cost, (node_row, node_col - 3), \
                Direction.WEST)))   
        # Eastbound nodes
        if node_col < map_width - 1:
            e1_cost = node.cost + map[node_row][node_col + 1]
            h = heuristic((node_row, node_col + 1), goal)
            open_queue.put((e1_cost + h, \
                BlockNode(e1_cost, (node_row, node_col + 1), \
                Direction.EAST)))
        if node_col < map_width - 2:
            e2_cost = e1_cost + map[node_row][node_col + 2]
            h = heuristic((node_row, node_col + 2), goal)
            open_queue.put((e2_cost + h, \
                BlockNode(e2_cost, (node_row, node_col + 2), \
                Direction.EAST)))
        if node_col < map_width - 3:
            w3_cost = e2_cost + map[node_row][node_col + 3]
            h = heuristic((node_row, node_col + 3), goal)
            open_queue.put((w3_cost + h, \
                BlockNode(w3_cost, (node_row, node_col + 3), \
                Direction.EAST)))                        
