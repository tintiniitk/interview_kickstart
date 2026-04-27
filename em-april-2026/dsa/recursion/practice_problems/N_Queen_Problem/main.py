import sys

"""

N Queen Problem
Given an integer n, find all possible ways to position n queens on an n×n chessboard so that no two queens attack each other. A queen in chess can move horizontally, vertically, or diagonally.

Do solve the problem using recursion first even if you see some non-recursive approaches.

Example One
{
"n": 4
}
Output:

[
["--q-",
 "q---",
 "---q",
 "-q--"],

["-q--",
 "---q",
 "q---",
 "--q-"]
]
There are two distinct ways four queens can be positioned on a 4×4 chessboard without attacking each other. The positions may appear in the output in any order. So the same two positions in different order would be another correct output.

Example Two
{
"n": 2
}
Output:

[
]
No way to position two queens on a 2×2 chessboard without them attacking each other - so empty array.

Notes
The function must return a two-dimensional array of strings representing the arrangements. Size of the array must be m×n where m is the number of distinct arrangements.

Each string must be n characters long, and the strings' characters may be either q (for a queen) or - (for an empty position on the chessboard). Valid arrangements may appear in the output in any order.

Constraints:

1 <= n <= 12

"""

StrBoard = list[str]
StrBoards = list[StrBoard]


def print_strboard(board: StrBoard, name: str, prefix: str = ""):
    print(f"{prefix}{name}: ")
    for s in board:
        # print(f"{prefix}{s}")
        spaced_s = " ".join(s)
        print(f"{prefix}{spaced_s}")

def find_all_arrangements(n: int) -> StrBoards:
    """
    Args:
     n(int32)
    Returns:
     list_list_str
    """
    # Write your code here.

    boards = StrBoards()

    def board_from_queen_positions(qp: list[int]) -> list[str]:
        board = []
        for qpi in qp:
            board.append("".join(["-"] * qpi + ["q"] + ["-"] * (n - 1 - qpi)))
        return board

    queen_positions = []
    columns_occupied = []
    positive_diagonals_occupied = []
    negative_diagnoals_occupied = []

    def solve(row: int):
        prefix = f"{'.'*row}"
        # print(
        #     f"{prefix} solve({row}, queen_positions={queen_positions}, columns_occupied={columns_occupied}, positive_diagonals_occupied={positive_diagonals_occupied}, negative_diagnoals_occupied={negative_diagnoals_occupied})"
        # )
        if row == n:
            # print(f"{prefix}  returning {queen_positions}")
            boards.append(board_from_queen_positions(queen_positions))
            return
        for col in range(n):
            if col not in columns_occupied:
                columns_occupied.append(col)
                if (row + col) not in positive_diagonals_occupied:
                    positive_diagonals_occupied.append(row + col)
                    if (row - col) not in negative_diagnoals_occupied:
                        negative_diagnoals_occupied.append(row - col)
                        queen_positions.append(col)
                        solve(row + 1)
                        queen_positions.pop()
                        negative_diagnoals_occupied.pop()
                    positive_diagonals_occupied.pop()
                columns_occupied.pop()

    solve(0)
    return boards


if __name__ == "__main__":
    n = 3
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    arrangements = find_all_arrangements(n)
    # print(f"n={n} => #arrangements = {len(arrangements)}")
    # for i, arrangement in enumerate(arrangements):
    #     print_strboard(arrangement, f"arrangement[{i}]", "  ")
    # pass
