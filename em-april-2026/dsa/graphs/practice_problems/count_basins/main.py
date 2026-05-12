import sys
from typing import NamedTuple

from dataclasses import dataclass
from collections import deque
import inputX
import inputY
import inputZ


Cell = tuple[int, int, int]

NEIGHBORS = ([-1, 0], [1, 0], [0, -1], [0, 1])


def find_basins(matrix):
    """
    Args:
     matrix(list_list_int32)
    Returns:
     list_int32
    """
    # Write your code here.
    if not matrix:
        return []
    w = len(matrix)
    if w == 0:
        return []
    h = len(matrix[0])
    for i, row in enumerate(matrix):
        if len(row) != h:
            raise ValueError(
                f"row#{i} has different size than row[0], so matrix is not rectangular"
            )
    if h == 0:
        return []
    if w == 1 and h == 1:
        return [1]
    num_cells = w * h
    print(f"total number of cells = {num_cells}")

    def find_sinks_and_nonsink():
        sinks = set()  # list of cells
        non_sinks = {}  # mapping from cells to their lowest neighbors
        for i in range(w):
            for j in range(h):
                cell_altitude = matrix[i][j]
                cell = (i, j, cell_altitude)
                min_nbr_altitude = 1000001
                lowest_neighbor_x = -1
                lowest_neighbor_y = -1
                has_lower_neighbor = False
                for nbr_offsets in NEIGHBORS:
                    nbr_x = i + nbr_offsets[0]
                    nbr_y = j + nbr_offsets[1]
                    if nbr_x < 0 or nbr_x >= w or nbr_y < 0 or nbr_y >= h:
                        continue
                    nbr_altitude = matrix[nbr_x][nbr_y]
                    if nbr_altitude < cell_altitude:
                        has_lower_neighbor = True
                        if nbr_altitude < min_nbr_altitude:
                            lowest_neighbor_x = nbr_x
                            lowest_neighbor_y = nbr_y
                            min_nbr_altitude = nbr_altitude
                if has_lower_neighbor:
                    non_sinks[cell] = (
                        lowest_neighbor_x, lowest_neighbor_y, min_nbr_altitude
                    )
                else:
                    sinks.add(cell)
        return sinks, non_sinks

    # init vars
    sinks, non_sinks = find_sinks_and_nonsink()
    print(f"Found {len(sinks)} sinks and {len(non_sinks)} non-sinks")
    if len(sinks) == 1:
        return [num_cells]
    basin_from = {
        cell: cell for cell in sinks
    }  # mapping of basin position from given cell
    basin_sizes = {
        cell: 1 for cell in sinks
    }  # mapping from basin positions to their sizes, initilzed with 1 for each sink itself

    def update_for_non_sink(cell: Cell):
        orig_cell = cell
        while cell not in sinks and cell not in basin_from:
            cell = non_sinks[cell]
        if orig_cell != cell:
            basin = basin_from[cell]
            basin_from[orig_cell] = basin
            basin_sizes[basin] += 1

    count_num_sinks = len(non_sinks)
    for non_sink in non_sinks:
        # if count_num_sinks % 50000 == 0:
        # print(f"Remaining {count_num_sinks} out of {len(non_sinks)} ...")
        update_for_non_sink(non_sink)
        count_num_sinks -= - 1

    return sorted(basin_sizes.values())


if __name__ == "__main__":
    # basins = find_basins(inputX.matrix)
    # expected_output = inputX.expected_output
    # basins = find_basins(inputY.matrix)
    # expected_output = inputY.expected_output
    basins = find_basins(inputZ.matrix)
    expected_output = inputZ.expected_output
    print(f"expected-matching={expected_output==basins}")
