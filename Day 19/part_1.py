from __future__ import annotations
import re

# A basic struct with four named int values
class XMASValue:
    regex = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
    def __init__(self, s: str) -> None:
        parts = self.regex.match(s).group
        self.x = int(parts(1))
        self.m = int(parts(2))
        self.a = int(parts(3))
        self.s = int(parts(4))

# The Router class and its subclasses are used to build
# the processing pipelines used in the network nodes.
class Router:
    def next(self, val: XMASValue) -> NetworkNode:
        return None

class Comparison(Router):
    def __init__(self, parameter: str, type: str, cutoff: int, destination: NetworkNode) -> None:
        super().__init__()
        self.parameter = parameter # x, m, a, or s
        self.type = type # < or >
        self.cutoff = cutoff
        self.destination = destination

    def next(self, val: XMASValue) -> NetworkNode:
        i_val: int
        if self.parameter == "x":
            i_val = val.x
        elif self.parameter == "m":
            i_val = val.m
        elif self.parameter == "a":
            i_val = val.a
        elif self.parameter == "s":
            i_val = val.s
        
        if self.type == "<":
            if i_val < self.cutoff:
                return self.destination
            else:
                return None
        else:
            if i_val > self.cutoff:
                return self.destination
            else:
                return None

class Redirect(Router):
    def __init__(self, destination: NetworkNode) -> None:
        super().__init__()
        self.destination = destination

    def next(self, val: XMASValue) -> NetworkNode:
        return self.destination

# The NetworkNode and its subclasses are used
# to build a graph.
class NetworkNode:
    def __init__(self) -> None:
        pass

    def insert(self, val: XMASValue):
        pass

class Pipeline(NetworkNode):
    compare_regex = re.compile(r"([xmas])([<>])(\d+):(\w+)")
    def __init__(self) -> None:
        super().__init__()
        self.pipeline: [Router] = []

    def setup(self, code: str, name_hash: {str:NetworkNode}) -> None:
        # Break the code into the pipeline steps
        steps = code.split(",")
        # The last option is the default value to redirect to
        default_node = Redirect(name_hash[steps.pop()])
        # Make the other steps into comparison routers
        for step in steps:
            p = self.compare_regex.match(step).group
            compare = Comparison(p(1), p(2), int(p(3)), name_hash[p(4)])
            self.pipeline.append(compare)
        self.pipeline.append(default_node)

    # Take in a value, and insert it into the next node
    def insert(self, val: XMASValue):
        # Check each router in the pipeline, until one returns another node
        for router in self.pipeline:
            if (next := router.next(val)) is not None:
                next.insert(val)
                break    

class Collector(NetworkNode):
    def __init__(self) -> None:
        super().__init__()
        self.count: int = 0

    # This is an end node, so add to the
    # internal count.
    def insert(self, val: XMASValue):
        self.count += val.x
        self.count += val.m
        self.count += val.a
        self.count += val.s


data_file = open("data.txt").read()
file_parts = data_file.split("\n\n")
schematic = file_parts[0].splitlines()
data = file_parts[1].splitlines()

# Process the first part of the input data,
# making a network of nodes to process the data
accepted = Collector()
rejected = Collector()
in_node : Pipeline = None
node_hash = {"A": accepted, "R": rejected}
code_hash = {}

line_regex = re.compile(r"(\w+)\{(.+)\}")


# Create the pipelines, and store the code used to program them
for node_def in schematic:
    line_parts = line_regex.match(node_def).group
    node_name = line_parts(1)
    node_code = line_parts(2)
    new_pipeline = Pipeline()
    node_hash[node_name] = new_pipeline
    code_hash[node_name] = node_code
    if node_name == "in":
        in_node = new_pipeline

# Use the code to build the pipelines
for node_name, node_code in code_hash.items():
    this_node: Pipeline = node_hash[node_name]
    this_node.setup(node_code, node_hash)

# Process the data lines
for val in data:
    xmas = XMASValue(val)
    in_node.insert(xmas)

print("Score: %d" % accepted.count)



