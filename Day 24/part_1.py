import numpy as np

data_rows = open("data.txt").read().splitlines()

class Line2D:
    def __init__(self, x: int, y: int, dx: int, dy: int) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def intersection_with(self, other):
        # Define a matrix to solve the problem with linear algebra.
        m = np.array([[other.dy, -1*self.dy], [other.dx, -1*self.dx]])
        # A singular matrix represents parallel lines
        if np.linalg.det(m) == 0:
            return None
        v = np.array([self.y - other.y, self.x - other.x])
        m_inv = np.linalg.inv(m)
        times = m_inv.dot(v)
        # Negative times are not valid
        if times[0] < 0 or times[1] < 0:
            return None
        # Solve for the actual position and return
        return(self.x + times[1] * self.dx, self.y + times[1] * self.dy)

    def __str__(self) -> str:
        return "(%d, %d) @ (%d, %d)" % (self.x, self.y, self.dx, self.dy)
    
    def __repr__(self) -> str:
        return "(%d, %d) @ (%d, %d)" % (self.x, self.y, self.dx, self.dy)
    
lines: [Line2D] = []

for stone in data_rows:
    parts = stone.split(" @ ")
    position = parts[0].split(", ")
    velocity = parts[1].split(", ")

    new_line = Line2D(int(position[0]), int(position[1]), int(velocity[0]), int(velocity[1]))
    lines.append(new_line)

sum = 0
min_dim = 200000000000000
max_dim = 400000000000000
for i in range(len(lines) - 1):
    for j in range(i + 1, len(lines)):
        if (pos := lines[i].intersection_with(lines[j])) is not None:
            if pos[0] >= min_dim and pos[0] <= max_dim \
            and pos[1] >= min_dim and pos[1] <= max_dim:
                sum += 1

print("Sum: %d" % sum)