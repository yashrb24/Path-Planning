import queue
import random
import cv2 as cv
import numpy as np
from collections import defaultdict

# the setup for maze
maze = np.zeros((50, 50, 3), dtype="uint8")
maze[:] = 255, 255, 255
width, height = maze.shape[0], maze.shape[1]

for i in range(width):
    for j in range(height):
        choice = random.choices([1, 0], weights=[1, 3], k=1)  # pixel is obstacle with probability 25%
        if choice == [1]:
            maze[i][j] = [0, 0, 0]  # make the obstacles black

# randomising start and end points
start_x, start_y = random.randint(0, width-1), random.randint(0, height-1)
while list(maze[start_x][start_y]) == [0, 0, 0]:
    start_x, start_y = random.randint(0, width), random.randint(0, height)
start = (start_x, start_y)

end_x, end_y = random.randint(0, width-1), random.randint(0, height-1)
while list(maze[end_x][end_y]) == [0, 0, 0]:
    end_x, end_y = random.randint(0, width), random.randint(0, height)
end = (end_x, end_y)


# helper functions

def adjacent(pt, VISITED):
    x, y = pt
    dr = [0, 0, 1, -1]
    dc = [1, -1, 0, 0]
    adj_pts = []
    for a, b in zip(dr, dc):
        rr, cc = x + a, y + b
        if not (0 <= rr < width and 0 <= cc < height):  # if the point is outside the map
            continue
        elif (rr, cc) in VISITED:  # if the point is already visited
            continue
        elif list(maze[rr][cc]) == [0, 0, 0]:  # if the point is an obstacle
            continue
        else:
            adj_pts.append((rr, cc))
    return adj_pts


def reconstruct_path(START, END, PARENT_DICT):
    curr = END
    while curr != START:
        curr = PARENT_DICT[curr]
        maze[curr[0]][curr[1]] = [0, 255, 0]


# sanity check
print(f"start: {start}")
print(f"end: {end}")

# the algorithm
gscore = defaultdict(lambda: int(1e6))
gscore[start] = 0

pq = queue.PriorityQueue()
pq.put((gscore[start], start))
visited = set()
came_from = {}

while pq.qsize() != 0:
    _, current = pq.get()
    if current == end:
        reconstruct_path(start, end, came_from)
        print("Path found!")
        print(f"path length is {gscore[end]}")
        break
    maze[current[0]][current[1]] = [0, 255, 255]
    neighbours = adjacent(current, visited)
    for neighbour in neighbours:
        temp_gscore = gscore[current] + 1
        if temp_gscore < gscore[neighbour]:
            came_from[neighbour] = current
            gscore[neighbour] = temp_gscore
            pq.put((gscore[neighbour], neighbour))

    visited.add(current)

maze[start_x][start_y] = [255, 0, 0]
maze[end_x][end_y] = [0, 0, 255]

maze = cv.resize(maze, (800, 700), interpolation=cv.INTER_AREA)
cv.imshow("maze", maze)
cv.waitKey(0)