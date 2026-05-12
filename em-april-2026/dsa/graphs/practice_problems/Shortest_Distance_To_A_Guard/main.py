"""

Shortest Distance To A Guard
You are given a two-dimensional character grid n by m. Each element of the grid is either a Guard, an Open space or a Wall. A guard can move up, down, left or right in the Open space. They cannot move on Walls.

For every Open space cell, find the shortest distance to the nearest guard.

Example One
{
"grid": [
["O", "O", "O", "O", "G"],
["O", "W", "W", "O", "O"],
["O", "O", "O", "W", "O"],
["G", "W", "W", "W", "O"],
["O", "O", "O", "O", "G"]
]
Output:

[
[3,  3,  2,  1,  0],
[2, -1, -1,  2,  1],
[1,  2,  3, -1,  2],
[0, -1, -1, -1,  1],
[1,  2,  2,  1,  0]
]
All Guard cells have zero distance to the nearest guard.
We consider the distance from the Wall cells to the nearest guard be -1.
For other (Open space) cells, we calculated the distance.

Example Two
{
"grid": [
["G", "W", "O", "W", "G"]
]
}
Output:

[
[0, -1, -1, -1, 0]
]
The Open space cell in the middle is unreachable for guards, so the distance is considered to be -1.

Notes
In the input grid, "G" represents a guard, "O" represents open space, and "W" represents a wall.
Output is a two-dimensional array of integers, n by m.
Constraints:

1 <= n, m <= 10^3

"""

import sys
from dataclasses import dataclass
from collections import deque
import inputX
import inputY

NEIGHBOR_OFFSETS = ((-1, 0), (1, 0), (0, -1), (0, 1))
MAX_DISTANCE = 1000001


def print_grid(grid: list[list[int]], name: str = "grid"):
    print(f"{name} = ")
    for row in grid:
        print(row)


# @profile
def find_shortest_distance_from_a_guard(grid):
    """
    Args:
     grid(list_list_char)
    Returns:
     list_list_int32
    """
    # Write your code here.
    if not grid:
        return grid
    w = len(grid)
    if w < 1:
        return grid
    h = len(grid[0])
    if h < 1:
        return grid
    if any(not row or len(row) != h for row in grid):
        raise ValueError(f"grid isn't a rectangle")
    # print_grid(grid)

    ret = [
        [
            (-1 if val == "W" else (0 if val == "G" else MAX_DISTANCE))
            for j, val in enumerate(row)
        ]
        for i, row in enumerate(grid)
    ]
    # print_grid(ret, "initial ret")

    guards = set()
    walls = set()
    opens = set()
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == "G":
                guards.add((i, j))
            elif val == "W":
                walls.add((i, j))
            else:
                opens.add((i, j))

    # @profile
    def valid_neighbors(node_x: int, node_y: int, dist: int) -> list[tuple[int]]:
        ret = []
        for nbr_offset in NEIGHBOR_OFFSETS:
            nbr_x = node_x + nbr_offset[0]
            nbr_y = node_y + nbr_offset[1]
            if nbr_x < 0 or nbr_x >= w or nbr_y < 0 or nbr_y >= h:
                continue
            if grid[nbr_x][nbr_y] in ["W", "G"]:
                continue
            ret.append((nbr_x, nbr_y, dist))
        return ret

    for guard in guards:
        guard_x = guard[0]
        guard_y = guard[1]
        # visited = set()
        neighbors = valid_neighbors(guard_x, guard_y, 1)
        # print(f"Original set of neighbors of guard = {neighbors}")
        q = deque(neighbors)
        for nbr in neighbors:
            ret[nbr[0]][nbr[1]] = 1
        while len(q) > 0:
            node = q.popleft()
            # if (node[0], node[1]) not in visited:
            #     continue
            # visited.add((node[0], node[1]))
            neighbors = valid_neighbors(node[0], node[1], node[2])
            for neighbor in neighbors:
                nbr_x = neighbor[0]
                nbr_y = neighbor[1]
                nbr_distance = neighbor[2]
                min_distance = ret[nbr_x][nbr_y]
                new_min_distance = nbr_distance + 1
                if new_min_distance < min_distance:
                    min_distance = new_min_distance
                    ret[nbr_x][nbr_y] = min_distance
                    q.append((nbr_x, nbr_y, min_distance))
        # print_grid(ret, f"intermediate grid after impact of guard {guard} ")

    # replace all remaining open cells (blocked by walls) with -1
    for i in range(w):
        for j in range(h):
            if ret[i][j] == MAX_DISTANCE:
                ret[i][j] = -1

    return ret


if __name__ == "__main__":
    grid = [
        ["O", "O", "O", "O", "G"],
        ["O", "W", "W", "O", "O"],
        ["O", "O", "O", "W", "O"],
        ["G", "W", "W", "W", "O"],
        ["O", "O", "O", "O", "G"],
    ]
    expected_output = [
        [3, 3, 2, 1, 0],
        [2, -1, -1, 2, 1],
        [1, 2, 3, -1, 2],
        [0, -1, -1, -1, 1],
        [1, 2, 2, 1, 0],
    ]
    # grid = inputX.grid
    # expected_output = inputX.expected_output
    grid = inputY.grid
    expected_output = inputY.expected_output
    ret = find_shortest_distance_from_a_guard(grid)
    # print_grid(ret, "final grid")
    # print_grid(expected_output, "expected output")
    print(
        f"final grid matches={ret==expected_output} len(ret)={len(ret)}, len(expected_output)={len(expected_output)}"
        # f"final grid matches={ret==expected_output} dims(ret)={len(ret)} x {len(ret[0])}, dims(expected_output)={len(expected_output)} x {len(expected_output[0])}"
    )
    pass
