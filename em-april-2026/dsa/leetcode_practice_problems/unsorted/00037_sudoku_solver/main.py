from typing import List

SIZE = 9
BOX_SIZE = 3

def print_board(iboard: list[list[int]], title: str="", level: int = 0):
    if title:
        print(f"\n{title} = ")
    print(f"{'  '*level}---------------------------------")
    for row in iboard:
        print(f"{'  '*level}{' | '.join(map(lambda i: ('.' if i==0 else str(i)), row))}")
        print(f"{'  '*level}---------------------------------")


class Solution:
    def solveSudoku(self, iboard: List[List[str]]) -> None:
        """
        Do not return anything, modify iboard in-place instead.
        """
        ideal_row = set(list(range(1,SIZE+1)))
        iboard = [list(map(lambda cell_str: 0 if cell_str == '.' else int(cell_str) , row)) for row in iboard]
        # print(f"iboard={iboard}")
        print_board(iboard, "Original iboard")
        level = 0

        def possible_values_for_cell(i, j) -> list[int]:
            nonlocal iboard
            nonlocal level
            if iboard[i][j] == 0:
                values_already_present = set(iboard[i])
                for k in range(j):
                    values_already_present.add(iboard[k][j])
                for k in range(j+1,9):
                    values_already_present.add(iboard[k][j])
                box_i = (i // BOX_SIZE) * BOX_SIZE
                box_j = (j // BOX_SIZE) * BOX_SIZE
                for cell_i in range(BOX_SIZE):
                    for cell_j in range(BOX_SIZE):
                        values_already_present.add(iboard[box_i+cell_i][box_j+cell_j])
                return ideal_row - values_already_present - {0}
            return [iboard[i][j]]

        def unfilled_neighbors(i, j) -> set[tuple[int, int]]:
            nonlocal iboard
            nonlocal level
            unfld_nbrs = {(i,j)}
            for k in range(i):
                if iboard[k][j] == 0:
                    unfld_nbrs.add((k, j))
            for k in range(i+1,SIZE):
                if iboard[k][j] == 0:
                    unfld_nbrs.add((k, j))
            for k in range(j):
                if iboard[i][k] == 0:
                    unfld_nbrs.add((i, k))
            for k in range(j+1,SIZE):
                if iboard[i][k] == 0:
                    unfld_nbrs.add((i, k))
            box_i = (i // BOX_SIZE) * BOX_SIZE
            box_j = (j // BOX_SIZE) * BOX_SIZE
            for cell_i in range(BOX_SIZE):
                for cell_j in range(BOX_SIZE):
                    if iboard[box_i+cell_i][box_j+cell_j] == 0:
                        unfld_nbrs.add((box_i+cell_i,box_j+cell_j))
            return unfld_nbrs - {(i,j)}

        def solve(i, j) -> bool:
            nonlocal iboard
            nonlocal level
            if 1 <= iboard[i][j] <= SIZE:
                return # nothing to be done
            if iboard[i][j] > SIZE or iboard[i][j] < 0:
                raise ValueError(f"Found iboard[{i}][{j}] > {SIZE} or < 0") # can't handle
            if iboard[i][j] == 0:
                print(f"{'  '*level}at i,j={i},{j}")
                possible_values = possible_values_for_cell(i, j)
                print(f"{'  '*level}found possible_values={possible_values}")
                if not possible_values:
                    return False
                unfld_nbrs = unfilled_neighbors(i, j)
                print(f"{'  '*level}unfld_nbrs={unfld_nbrs}")
                any_value_worked = False
                for possible_value in possible_values:
                    iboard[i][j] = possible_value
                    level += 1
                    # print_board(iboard, "iboard so far", level)
                    for unfld_nbr_i, unfld_nbr_j in unfld_nbrs:
                        if not solve(unfld_nbr_i, unfld_nbr_j):
                            iboard[i][j] = 0
                            level -= 1
                            try_next_value = True
                            break
                    # undo
                    if not try_next_value:
                        any_value_worked = True
                        if level > 0:
                            iboard[i][j] = 0
                            level -= 1
                            # print_board(iboard, "backtracked iboard so far", level)
                        else:
                            # print_board(iboard, "board after fixing {i},{j}", level)
                            pass
                        break
            return any_value_worked

        for i in range(SIZE):
            for j in range(SIZE):
                if iboard[i][j] == 0:
                    level = 0
                    print(f"Starting a new DFS filling from {i},{j} ...")
                    if not solve(i,j):
                        raise ValueError("Failed to solve sudoku!")

        for i in range(SIZE):
            for j in range(SIZE):
                board[i][j] = str(iboard[i][j])

        print_board(board, "final board", 0)

Solution().solveSudoku([["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]])
