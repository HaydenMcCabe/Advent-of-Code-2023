from __future__ import annotations
from queue import PriorityQueue
from enum import Enum

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

class BlockNode():
    def __init__(self, cost: int, location: (int, int), direction: Direction, distance: int, parent: BlockNode) -> None:
        self.cost = cost
        self.location = location
        self.direction = direction
        self.distance = distance
        self.parent = parent

    def __lt__(self, other) -> bool:
        return self.cost < other.cost
    
    def __str__(self) -> str:
        return "Cost: %d, (%d, %d), %s" % (self.cost, self.location[0], self.location[1], self.direction)

# Return the taxicab distance from the position to the goal
def heuristic(location: (int, int), goal: (int, int)) -> int:
    return (goal[0] - location[0]) + (goal[1] - location[1])

# Convert the input text into an array of integers
data = open("data.txt").read().splitlines()
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
# Make lists to track open and closed locations
open_list: {any: int} = {}
closed_list: {any: int} = {}
# At the beginning is the only time the options aren't
# on a straight line, so add them manually.

e1 = BlockNode(map[0][1], (0,1), Direction.EAST, 1, None)
e2 = BlockNode(map[0][1] + map[0][2], (0,2), Direction.EAST, 2, None)
e3 = BlockNode(map[0][1] + map[0][2] + map[0][3], (0,3), Direction.EAST, 3, None)

e1_f = heuristic(e1.location, goal) + e1.cost
e2_f = heuristic(e2.location, goal) + e2.cost
e3_f = heuristic(e3.location, goal) + e3.cost

s1 = BlockNode(map[1][0], (1,0), Direction.SOUTH, 1, None)
s2 = BlockNode(map[1][0] + map[2][0], (2,0), Direction.SOUTH, 2, None)
s3 = BlockNode(map[1][0] + map[2][0] + map[3][0], (3,0), Direction.SOUTH, 3, None)

s1_f = heuristic(s1.location, goal) + s1.cost
s2_f = heuristic(s2.location, goal) + s2.cost
s3_f = heuristic(s3.location, goal) + s3.cost

open_queue.put((e1_f, e1))
open_queue.put((e2_f, e2))
open_queue.put((e3_f, e3))
open_queue.put((s1_f, s1))
open_queue.put((s2_f, s2))
open_queue.put((s3_f, s3))

open_list[(e1.location[0], e1.location[1], Direction.EAST, 1)] = e1_f
open_list[(e2.location[0], e2.location[1], Direction.EAST, 2)] = e2_f
open_list[(e3.location[0], e3.location[1], Direction.EAST, 3)] = e3_f
open_list[(s1.location[0], s1.location[1], Direction.SOUTH, 1)] = s1_f
open_list[(s2.location[0], s2.location[1], Direction.SOUTH, 2)] = s2_f
open_list[(s3.location[0], s2.location[1], Direction.SOUTH, 3)] = s3_f


while not open_queue.empty():
    node: BlockNode
    this_f, node = open_queue.get()
    this_key = (node.location[0], node.location[1], node.direction, node.distance)
    # print("Checking from location (%d, %d) with f score %d" % (node.location[0], node.location[1], this_f))
    # print("Open list: %s" % open_list)
    # print("Closed list: %s" % closed_list)
    # print()

    if (closed_f_for_location := closed_list.get(this_key, None)) is not None:
        if closed_f_for_location < this_f:
            continue
        
    # Also remove this location from the open list
    del open_list[this_key]

    node_row = node.location[0]
    node_col = node.location[1]
    
    # The lowest cost path has been found if the
    # goal node is the highest priority.
    if node.location == goal:
        print("Cost: %d" % node.cost)
        break

    # Collect tuples of the new nodes and their f score
    new_nodes = []

    # There are as many as six nodes that can be reached
    # from the current node
    if node.direction == Direction.EAST or node.direction == Direction.WEST:
        # Northbound nodes
        if node_row > 0:
            n1_cost = node.cost + map[node_row - 1][node_col]
            h = heuristic((node_row - 1, node_col), goal)
            n1 = BlockNode(n1_cost, (node_row - 1, node_col), \
                Direction.NORTH, 1, node)
            new_nodes.append((n1_cost + h, n1))
        if node_row > 1:
            n2_cost = n1_cost + map[node_row - 2][node_col]
            h = heuristic((node_row - 2, node_col), goal)
            n2 = BlockNode(n2_cost, (node_row - 2, node_col), \
                Direction.NORTH, 2, node)
            new_nodes.append((n2_cost + h, n2))
        if node_row > 2:
            n3_cost = n2_cost + map[node_row - 3][node_col]
            h = heuristic((node_row - 3, node_col), goal)
            n3 = BlockNode(n3_cost, (node_row - 3, node_col), \
                Direction.NORTH, 3, node)
            new_nodes.append((n3_cost + h, n3))
        # Southbound nodes
        if node_row < map_height - 1:
            s1_cost = node.cost + map[node_row + 1][node_col]
            h = heuristic((node_row + 1, node_col), goal)
            s1 = BlockNode(s1_cost, (node_row + 1, node_col), \
                Direction.SOUTH, 1, node)
            new_nodes.append((s1_cost + h, s1))
        if node_row < map_height - 2:
            s2_cost = s1_cost + map[node_row + 2][node_col]
            h = heuristic((node_row + 2, node_col), goal)
            s2 = BlockNode(s2_cost, (node_row + 2, node_col), \
                Direction.SOUTH, 2, node)
            new_nodes.append((s2_cost + h, s2))
        if node_row < map_height - 3:
            s3_cost = s2_cost + map[node_row + 3][node_col]
            h = heuristic((node_row + 3, node_col), goal)
            s3 = BlockNode(s3_cost, (node_row + 3, node_col), \
                Direction.SOUTH, 3, node)
            new_nodes.append((s3_cost + h, s3))
    else:
         # Westbound nodes
        if node_col > 0:
            w1_cost = node.cost + map[node_row][node_col - 1]
            h = heuristic((node_row, node_col - 1), goal)
            w1 = BlockNode(w1_cost, (node_row, node_col - 1), \
                Direction.WEST, 1, node)
            new_nodes.append((w1_cost + h, w1))
        if node_col > 1:
            w2_cost = w1_cost + map[node_row][node_col - 2]
            h = heuristic((node_row, node_col - 2), goal)
            w2 = BlockNode(w2_cost, (node_row, node_col - 2), \
                Direction.WEST, 2, node)
            new_nodes.append((w2_cost + h, w2))
        if node_col > 2:
            w3_cost = w2_cost + map[node_row][node_col - 3]
            h = heuristic((node_row, node_col - 3), goal)
            w3 = BlockNode(w3_cost, (node_row, node_col - 3), \
                Direction.WEST, 3, node)
            new_nodes.append((w3_cost + h, w3))
        # Eastbound nodes
        if node_col < map_width - 1:
            e1_cost = node.cost + map[node_row][node_col + 1]
            h = heuristic((node_row, node_col + 1), goal)
            e1 = BlockNode(e1_cost, (node_row, node_col + 1), \
                Direction.EAST, 1, node)
            new_nodes.append((e1_cost + h, e1))
        if node_col < map_width - 2:
            e2_cost = e1_cost + map[node_row][node_col + 2]
            h = heuristic((node_row, node_col + 2), goal)
            e2 = BlockNode(e2_cost, (node_row, node_col + 2), \
                Direction.EAST, 2, node)
            new_nodes.append((e2_cost + h, e2))
        if node_col < map_width - 3:
            e3_cost = e2_cost + map[node_row][node_col + 3]
            h = heuristic((node_row, node_col + 3), goal)
            e3 = BlockNode(e3_cost, (node_row, node_col + 3), \
                Direction.EAST, 3, node)
            new_nodes.append((e3_cost + h, e3))
    # Check the new nodes to see if they should be added to the open queue
    for f, new_node in new_nodes:
        new_key = (new_node.location[0], new_node.location[1], new_node.direction, new_node.distance)
        # There is an existing record in the open queue for this location.
        # If the existing record has a better or equal f score, continue
        if (existing_f_for_location := open_list.get(new_key, None)) is not None:
            # print(existing_f_for_location)
            if existing_f_for_location <= f:
                continue
        # If this location has already been considered with a lower f score, continue
        if (closed_f_for_location := closed_list.get(new_key, None)) is not None:
            if closed_f_for_location <= f:
                continue
        # Add to the queue
        open_queue.put((f, new_node))
        
        open_list[new_key] = f
    # Close this location for this f score
    closed_list[this_key] = this_f
    
        


            

