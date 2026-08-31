class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        m = len(matrix)
        n = len(matrix[0])
        if m == 1:
            return matrix[0]
        if n == 1:
            return [matrix[row][0] for row in range(m)]

        top_row, bottom_row, left_col, right_col = -1, m, -1, n
        ret = []
        while True:
            # print(f"started a new loop at top_row, bottom_row, left_col, right_col = {(top_row, bottom_row, left_col, right_col)}")
            # top-row
            i = top_row + 1
            for j in range(left_col + 1, right_col):
                ret.append(matrix[i][j])
            top_row += 1
            # print(f"after printing top-row: {ret}")
            if top_row + 1 > bottom_row - 1:
                break

            j = right_col - 1
            for i in range(top_row + 1, bottom_row):
                ret.append(matrix[i][j])
            right_col -= 1
            # print(f"after printing right-col: {ret}")
            if left_col + 1 > right_col - 1:
                break

            i = bottom_row - 1
            for j in range(right_col - 1, left_col, -1):
                ret.append(matrix[i][j])
            bottom_row -= 1
            # print(f"after printing bottom-row: {ret}")
            if top_row + 1 > bottom_row - 1:
                break

            j = left_col + 1
            for i in range(bottom_row - 1, top_row, -1):
                ret.append(matrix[i][j])
            left_col += 1
            # print(f"after printing leftright-col: {ret}")
            if left_col + 1 > right_col - 1:
                break
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(matrix: list[list[int]], expected: list[int]) -> tuple[bool, str]:
    actual = Solution().spiralOrder(matrix)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                expected=[1, 2, 3, 6, 9, 8, 7, 4, 5],
            )
            Test(
                matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                expected=[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
            )
            Test(matrix=[[1, 2, 3, 4], [5, 6, 7, 8]], expected=[1, 2, 3, 4, 8, 7, 6, 5])
            Test(
                matrix=[[1, 2], [3, 4], [5, 6], [7, 8]],
                expected=[1, 2, 4, 6, 8, 7, 5, 3],
            )
            Test(matrix=[[2, 3]], expected=[2, 3])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
