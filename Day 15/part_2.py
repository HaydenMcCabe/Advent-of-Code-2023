import re

def dumb_hash(s: str):
    ascii_values = list(s.encode("ascii"))
    hash_val = 0
    for val in ascii_values:
        hash_val += val
        hash_val *= 17
        hash_val &= 0xff
    return hash_val

class lens:
    def __init__(self, label: str, focus: int) -> None:
        self.label = label
        self.focus = focus

def remove_lens(label: str, arr: [lens]):
    print(arr)
    arr = list(filter(lambda e: e.label == label, arr))


boxes = [[] for i in range(256)]

input = open("data.txt").read().split(",")

command_regex = re.compile(r"(\w+)(\-|=(\d))")
for command in input:
    parsed = command_regex.match(command)
    label = parsed.group(1)
    label_hash = dumb_hash(label)
    if parsed.group(2)[0] == "-":
        old_values = boxes[label_hash]
        boxes[label_hash] = list(filter(lambda e: e.label != label, old_values))
    else:
        # Add or update a lens
        new_lens = lens(label, int(parsed.group(3)))
        broken = False
        for i in range(len(boxes[label_hash])):
            if boxes[label_hash][i].label == label:
                boxes[label_hash][i] = new_lens
                broken = True
                break
        if not broken:
            boxes[label_hash].append(new_lens)
        
sum = 0
for box_num in range(256):
    box = boxes[box_num]
    for lens_num in range(len(box)):
        lens = box[lens_num]
        sum += (box_num + 1) * (lens_num + 1) * (lens.focus)

print("Sum: %d" % sum)