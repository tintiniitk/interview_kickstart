"""

Sudoku Solver
Given a partially filled two-dimensional array, fill all the unfilled cells such that each row, each column and each 3 x 3 subgrid (as highlighted below by bolder lines) has every digit from 1 to 9 exactly once.

Unfilled cells have a value of 0 on the given board.

Example
Example one

{
"board": [
[8, 4, 9, 0, 0, 3, 5, 7, 0],
[0, 1, 0, 0, 0, 0, 0, 0, 0],
[7, 0, 0, 0, 9, 0, 0, 8, 3],
[0, 0, 0, 9, 4, 6, 7, 0, 0],
[0, 8, 0, 0, 5, 0, 0, 4, 0],
[0, 0, 6, 8, 7, 2, 0, 0, 0],
[5, 7, 0, 0, 1, 0, 0, 0, 4],
[0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 2, 1, 7, 0, 0, 8, 6, 5]
]
}
Output:

[
[8, 4, 9, 1, 6, 3, 5, 7, 2],
[3, 1, 5, 2, 8, 7, 4, 9, 6],
[7, 6, 2, 4, 9, 5, 1, 8, 3],
[1, 5, 3, 9, 4, 6, 7, 2, 8],
[2, 8, 7, 3, 5, 1, 6, 4, 9],
[4, 9, 6, 8, 7, 2, 3, 5, 1],
[5, 7, 8, 6, 1, 9, 2, 3, 4],
[6, 3, 4, 5, 2, 8, 9, 1, 7],
[9, 2, 1, 7, 3, 4, 8, 6, 5]
]
Notes
You can assume that any given puzzle will have exactly one solution.

Constraints:

Size of the input array is exactly 9 x 9
0 <= value in the input array <= 9

"""

Board = list[list[int]]


def print_board(board: Board, name: str):
    print(f"{name} = ")
    for row in board:
        print(f"{row}")


def solve_sudoku_puzzle(board: Board) -> Board:
    """
    Args:
     board(list_list_int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    # make list of all cells not filled
    ideal_filled_list = list(range(1, 10))
    ideal_filled_set = set(ideal_filled_list)
    unfilled_cells = [
        (r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == 0
    ]
    print(f"unfilled_cells={unfilled_cells}")

    slate = [row[:] for row in board]

    def verify(board: Board) -> bool:
        if any(0 in row for row in board):
            return False
        for row in board:
            if not sorted(row) == ideal_filled_list:
                return False
        for col in zip(*board):
            if not sorted(col) == ideal_filled_list:
                return False
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                # flatten 3x3 grid into 9 values:
                box = [board[i][j] for i in range(r, r + 3) for j in range(c, c + 3)]
                if sorted(box) != ideal_filled_list:
                    return False
        return True

    def solve(unfilled_cell_index: int) -> bool:
        # print_board(slate, "slate")
        # print(
            # f"{'....'*unfilled_cell_index}solve({unfilled_cells[unfilled_cell_index:min(len(unfilled_cells), unfilled_cell_index+1)]})"
        # )
        if unfilled_cell_index == len(unfilled_cells):
            if verify(slate):
                # print("Found a valid board.")
                # print_board(slate, "slate")
                for r in range(9):
                    for c in range(9):
                        board[r][c] = slate[r][c]
            return True

        r, c = unfilled_cells[unfilled_cell_index]
        # check if (r,c) is solvable
        # get the set of the values in the row r
        row = [val for val in slate[r] if val != 0]
        if any((v < 1 or v > 9) for v in row):
            return False
        row_set = set(row)
        if len(row) != len(row_set):
            return False
        # get the set of the values in the column c
        column = [row[c] for row in slate if row[c] != 0]
        if any((v < 1 or v > 9) for v in column):
            return False
        column_set = set(column)
        if len(column) != len(column_set):
            return False
        # get the set of values in the cells containing (r,c)
        box = [
            slate[i][j]
            for i in range(3 * (r // 3), 3 * (1 + (r // 3)))
            for j in range(3 * (c // 3), 3 * (1 + (c // 3)))
            if slate[i][j] > 0
        ]
        if any((v < 1 or v > 9) for v in box):
            return False
        box_set = set(box)
        if len(box) != len(box_set):
            return False
        # do union of all 3, and see if its size is 8.
        values_filled_so_far = row_set | column_set | box_set
        if len(values_filled_so_far) > 8:
            # print(f"No valid value remaining for ({r},{c})")
            return False
        else:
            unfilled_values = list(ideal_filled_set - values_filled_so_far)
            # print(f"Candidates for ({r},{c}) = {unfilled_values}")
            for unfilled_value in unfilled_values:
                slate[r][c] = unfilled_value
                if solve(unfilled_cell_index + 1):
                    slate[r][c] = 0
                    return True
                else:
                    slate[r][c] = 0
            return False

    if solve(0):
        return board
    print(f"Failed to solve board")
    # print_board(board, "board")
    return board


if __name__ == "__main__":
    board = [
        [8, 4, 9, 0, 0, 3, 5, 7, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 9, 0, 0, 8, 3],
        [0, 0, 0, 9, 4, 6, 7, 0, 0],
        [0, 8, 0, 0, 5, 0, 0, 4, 0],
        [0, 0, 6, 8, 7, 2, 0, 0, 0],
        [5, 7, 0, 0, 1, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 2, 1, 7, 0, 0, 8, 6, 5],
    ]
    solve_sudoku_puzzle(board)
    # print(f"solved sudoku board = ")
    # print_board(board, "board")
