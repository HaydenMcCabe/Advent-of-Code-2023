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
east_cost = map[0][1] + map[0][2] + map[0][3]
for east_distance in range(4, 11):
    east_col = 0 + east_distance
    if east_col >= map_width:
        break
    east_cost += map[0][east_col]
    new_node = BlockNode(east_cost, (0,east_col), Direction.EAST, east_distance, None)
    f = heuristic(new_node.location, goal) + east_cost
    open_queue.put((f, new_node))
    open_list[(new_node.location[0], new_node.location[1], new_node.direction, new_node.distance)] = f

south_cost = map[1][0] + map[2][0] + map[3][0]
for south_distance in range(4, 11):
    south_row = 0 + south_distance
    if south_row >= map_height:
        break
    south_cost += map[south_row][0]
    new_node = BlockNode(south_cost, (south_row,0), Direction.SOUTH, south_distance, None)
    f = heuristic(new_node.location, goal) + south_cost
    open_queue.put((f, new_node))
    open_list[(new_node.location[0], new_node.location[1], new_node.direction, new_node.distance)] = f


while not open_queue.empty():
    node: BlockNode
    this_f, node = open_queue.get()
    this_key = (node.location[0], node.location[1], node.direction, node.distance)

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

    # Consider each node that can be reached from here
    if node.direction == Direction.EAST or node.direction == Direction.WEST:
        # Northbound nodes
        if node_row >= 4:
            north_cost = node.cost + map[node_row - 1][node_col] + map[node_row - 2][node_col] + map[node_row - 3][node_col]
            for north_distance in range(4, 11):
                north_row = node_row - north_distance
                if north_row < 0:
                    break
                north_cost += map[north_row][node_col]
                new_node = BlockNode(north_cost, (north_row,node_col), Direction.NORTH, north_distance, node)
                f = heuristic(new_node.location, goal) + north_cost
                new_nodes.append((f, new_node))
        # Southbound nodes
        if node_row + 4 < map_height:
            south_cost = node.cost + map[node_row + 1][node_col] + map[node_row + 2][node_col] + map[node_row + 3][node_col]
            for south_distance in range(4, 11):
                south_row = node_row + south_distance
                if south_row >= map_height:
                    break
                south_cost += map[south_row][node_col]
                new_node = BlockNode(south_cost, (south_row,node_col), Direction.SOUTH, south_distance, node)
                f = heuristic(new_node.location, goal) + south_cost
                new_nodes.append((f, new_node))

    else:
        # Westbound nodes
        if node_col >= 4:
            west_cost = node.cost + map[node_row][node_col - 1] + map[node_row][node_col - 2] + map[node_row][node_col - 3]
            for west_distance in range(4, 11):
                west_col = node_col - west_distance
                if west_col < 0:
                    break
                west_cost += map[node_row][west_col]
                new_node = BlockNode(west_cost, (node_row,west_col), Direction.WEST, west_distance, node)
                f = heuristic(new_node.location, goal) + west_cost
                new_nodes.append((f, new_node))        
        # Eastbound nodes
        if node_col + 4 < map_width:
            east_cost = node.cost + map[node_row][node_col + 1] + map[node_row][node_col + 2] + map[node_row][node_col + 3]
            for east_distance in range(4, 11):
                east_col = node_col + east_distance
                if east_col >= map_width:
                    break
                east_cost += map[node_row][east_col]
                new_node = BlockNode(east_cost, (node_row,east_col), Direction.EAST, east_distance, node)
                f = heuristic(new_node.location, goal) + east_cost
                new_nodes.append((f, new_node))        

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
    
        


            

