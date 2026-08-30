class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        marked_rows = set()
        marked_cols = set()
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    marked_rows.add(i)
                    marked_cols.add(j)
        for row in marked_rows:
            for j in range(n):
                matrix[row][j] = 0
        for col in marked_cols:
            for i in range(m):
                matrix[i][col] = 0


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(matrix: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    Solution().setZeroes(matrix)
    actual = matrix
    if actual[:] != expected[:]:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                matrix=[[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                expected=[[1, 0, 1], [0, 0, 0], [1, 0, 1]],
            )
            Test(
                matrix=[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
                expected=[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
