import logging

# CONFIGURE LOGGING LEVEL DYNAMICALLY
# If DEBUG_MODE is True, the logger captures everything down to DEBUG.
# If False, it defaults to INFO, ignoring debug statements.
# log_level = logging.DEBUG
log_level = logging.INFO
logging.basicConfig(
    level=log_level,
    # format="%(asctime)s - [%(levelname)s] - %(message)s"
    format="[%(levelname)s] %(message)s",
)
# CREATE A LOGGER INSTANCE
logger = logging.getLogger(__name__)

from typing import List
import copy
from copy import deepcopy
import heapq
from heapq import heappop, heappush, heapify

SIZE = 9
BOX_SIZE = 3
CHR_GRID = List[List[str]]
INT_GRID = List[List[int]]
IDEAL_ROW = list(range(1, SIZE + 1))


def int_grid_to_chr_grid(iboard: INT_GRID) -> CHR_GRID:
    board = [["." for _ in range(SIZE)] for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            board[i][j] = str(iboard[i][j]) if 1 <= iboard[i][j] <= SIZE else "."
    return board


def chr_grid_to_int_grid(board: CHR_GRID) -> INT_GRID:
    iboard = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            iboard[i][j] = 0 if board[i][j] == "." else int(board[i][j])
    return iboard


def print_chr_board(board: CHR_GRID, title: str = "", level: int = 0) -> str:
    s = "\n"
    if title:
        s += f"{'  '*level}{title} = \n"
    s += f"{'  '*level}---------------------------------\n"
    for row in board:
        s += f"{'  '*level}{' | '.join(row)}\n"
        s += f"{'  '*level}---------------------------------\n"
    return s


def print_int_board(iboard: INT_GRID, title: str = "", level: int = 0) -> str:
    board = int_grid_to_chr_grid(iboard)
    return print_chr_board(board)


def validate_filled_sudoku_iboard(iboard: INT_GRID):
    for i, row in enumerate(iboard):
        if sorted(row) != IDEAL_ROW:
            logger.error(f"Row#{i} = {row} isn't proper")
            return False
    for j in range(9):
        col = [iboard[i][j] for i in range(9)]
        if sorted(col) != IDEAL_ROW:
            logger.error(f"Col#{j} isn't proper")
            return False
    for sub_cell_i in range(3):
        for sub_cell_j in range(3):
            sub_cell = [
                iboard[sub_cell_i * 3 + i][sub_cell_j * 3 + j]
                for i in range(3)
                for j in range(3)
            ]
            if sorted(sub_cell) != IDEAL_ROW:
                logger.error(f"Sub-cell#({sub_cell_i},{sub_cell_j}) isn't proper")
                return False
    return True


def validate_filled_sudoku_board(board: CHR_GRID):
    iboard = chr_grid_to_int_grid(board)
    return validate_filled_sudoku_iboard(iboard)


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify iboard in-place instead.
        """
        iboard = chr_grid_to_int_grid(board)
        level = 0
        ideal_row = set(IDEAL_ROW)

        def possible_values_for_cell(iboard, row, col) -> set[int]:
            nonlocal level
            if iboard[row][col] == 0:
                values_already_present = set(iboard[row])
                for k in range(col):
                    values_already_present.add(iboard[k][col])
                for k in range(col + 1, 9):
                    values_already_present.add(iboard[k][col])
                box_i = (row // BOX_SIZE) * BOX_SIZE
                box_j = (col // BOX_SIZE) * BOX_SIZE
                for cell_i in range(BOX_SIZE):
                    for cell_j in range(BOX_SIZE):
                        values_already_present.add(
                            iboard[box_i + cell_i][box_j + cell_j]
                        )
                return ideal_row - values_already_present - {0}
            return set()

        def unfilled_neighbors_of_cell(iboard, row, col) -> set[tuple[int, int]]:
            nonlocal level
            unfld_nbrs = {(row, col)}
            for k in range(row):
                if iboard[k][col] == 0:
                    unfld_nbrs.add((k, col))
            for k in range(row + 1, SIZE):
                if iboard[k][col] == 0:
                    unfld_nbrs.add((k, col))
            for k in range(col):
                if iboard[row][k] == 0:
                    unfld_nbrs.add((row, k))
            for k in range(col + 1, SIZE):
                if iboard[row][k] == 0:
                    unfld_nbrs.add((row, k))
            box_i = (row // BOX_SIZE) * BOX_SIZE
            box_j = (col // BOX_SIZE) * BOX_SIZE
            for cell_i in range(BOX_SIZE):
                for cell_j in range(BOX_SIZE):
                    if iboard[box_i + cell_i][box_j + cell_j] == 0:
                        unfld_nbrs.add((box_i + cell_i, box_j + cell_j))
            return unfld_nbrs - {(row, col)}

        def get_unfilled_cell_pq(iboard: INT_GRID):
            filled_cells = True
            while filled_cells:
                filled_cells = False
                for row in range(SIZE):
                    for col in range(SIZE):
                        cell_value = iboard[row][col]
                        if not (1 <= cell_value <= SIZE):
                            cell = (row, col)
                            possible_values = possible_values_for_cell(iboard, row, col)
                            num_possible_values_for_cell = len(possible_values)
                            if num_possible_values_for_cell == 1:
                                iboard[row][col] = possible_values.pop()
                                filled_cells = True
            unfilled_cells = []
            for row in range(SIZE):
                for col in range(SIZE):
                    cell_value = iboard[row][col]
                    if not (1 <= cell_value <= SIZE):
                        cell = (row, col)
                        possible_values = possible_values_for_cell(iboard, row, col)
                        num_possible_values_for_cell = len(possible_values)
                        unfilled_cells.append((num_possible_values_for_cell, cell))
            if unfilled_cells:
                heapify(unfilled_cells)
            return unfilled_cells

        def fill(iboard: INT_GRID, unfilled_cells, level: int = 0) -> bool:
            iter = 0
            logger.debug(print_int_board(iboard, "fill() called with ", level))
            log_prefix = f"{" "*level}"
            if unfilled_cells:
                while unfilled_cells:
                    num_possible_values_for_cell, unfilled_cell = heappop(
                        unfilled_cells
                    )
                    row, col = unfilled_cell
                    if 1 <= iboard[row][col] <= 9:
                        continue
                    possible_values_for_unfilled_cell = possible_values_for_cell(
                        iboard, row, col
                    )
                    num_possible_values_for_cell = len(
                        possible_values_for_unfilled_cell
                    )
                    if num_possible_values_for_cell == 0:
                        if level == 0:
                            logger.warning(
                                f"{log_prefix}found zero possible values for unfilled cell: {unfilled_cell}"
                            )
                        return False
                    unfilled_neighbors = unfilled_neighbors_of_cell(iboard, row, col)
                    if num_possible_values_for_cell == 1:
                        iboard[row][col] = possible_values_for_unfilled_cell.pop()
                    else:
                        iboard_copy = deepcopy(iboard)
                        for (
                            possible_value_for_cell
                        ) in possible_values_for_unfilled_cell:
                            iboard_copy[row][col] = possible_value_for_cell
                            unfilled_cells = get_unfilled_cell_pq(iboard_copy)
                            if not fill(iboard_copy, unfilled_cells, level + 1):
                                continue
                            else:
                                iboard[row][col] = possible_value_for_cell
                                iboard[:] = deepcopy(iboard_copy)
                                return True
                        iboard[row][col] = 0
                        if level == 0:
                            logger.error(
                                f"Could not fill cell {unfilled_cell} with any value !"
                            )
                        return False
            return True

        unfilled_cells = get_unfilled_cell_pq(iboard)
        if not fill(iboard, unfilled_cells):
            raise ValueError(f"Failed to fill grid")
        board[:] = deepcopy(int_grid_to_chr_grid(iboard))
        return None


def Test(board: CHR_GRID, expected: CHR_GRID):
    print(f"\n[RUN]")
    orig_board = deepcopy(board)
    logger.info(print_chr_board(orig_board, "Input board", 0))
    logger.info(print_chr_board(expected, "Expected solved board", 0))
    Solution().solveSudoku(board)
    solved = deepcopy(board)
    logger.info(print_chr_board(solved, "Solved board", 0))
    assert validate_filled_sudoku_board(solved), f"Failed"
    print(f"[DONE]\n")


Test(
    [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ],
    [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ],
)
Test(
    [
        [".", ".", "9", "7", "4", "8", ".", ".", "."],
        ["7", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", "2", ".", "1", ".", "9", ".", ".", "."],
        [".", ".", "7", ".", ".", ".", "2", "4", "."],
        [".", "6", "4", ".", "1", ".", "5", "9", "."],
        [".", "9", "8", ".", ".", ".", "3", ".", "."],
        [".", ".", ".", "8", ".", "3", ".", "2", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "6"],
        [".", ".", ".", "2", "7", "5", "9", ".", "."],
    ],
    [
        ["5", "1", "9", "7", "4", "8", "6", "3", "2"],
        ["7", "8", "3", "6", "5", "2", "4", "1", "9"],
        ["4", "2", "6", "1", "3", "9", "8", "7", "5"],
        ["3", "5", "7", "9", "8", "6", "2", "4", "1"],
        ["2", "6", "4", "3", "1", "7", "5", "9", "8"],
        ["1", "9", "8", "5", "2", "4", "3", "6", "7"],
        ["9", "7", "5", "8", "6", "3", "1", "2", "4"],
        ["8", "3", "2", "4", "9", "1", "7", "5", "6"],
        ["6", "4", "1", "2", "7", "5", "9", "8", "3"],
    ],
)
