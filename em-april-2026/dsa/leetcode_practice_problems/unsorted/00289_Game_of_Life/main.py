NEIGHBORS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Solution:
    def gameOfLife(self, board: list[list[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # encode old value in bit 0, and new value in bit 1
        m = len(board)
        n = len(board[0])

        # pass 1: populate new values in bit 1 from old values in bit 0
        def should_live(i: int, j: int):
            board[i][j] |= 2

        def should_die(i: int, j: int):
            board[i][j] &= 1

        for i in range(m):
            for j in range(n):
                is_live = board[i][j] & 1 != 0
                num_live_neighbors = 0
                for nbr_del_i, nbr_del_j in NEIGHBORS:
                    nbr_i, nbr_j = i + nbr_del_i, j + nbr_del_j
                    if (
                        0 <= nbr_i < m
                        and 0 <= nbr_j < n
                        and (board[nbr_i][nbr_j] & 1 != 0)
                    ):
                        num_live_neighbors += 1
                if is_live:
                    if num_live_neighbors < 2 or num_live_neighbors > 3:
                        should_die(i, j)
                    else:
                        should_live(i, j)
                elif num_live_neighbors == 3:
                    should_live(i, j)
                else:
                    should_die(i, j)
        print(board)

        # pass 2: populate old values (bit 0) from new values (bit 1).
        for i in range(m):
            for j in range(n):
                board[i][j] >>= 1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(board: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().gameOfLife(board)
    if board[:] != expected[:]:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                board=[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]],
                expected=[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]],
            )
            Test(board=[[1, 1], [1, 0]], expected=[[1, 1], [1, 1]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
