class Solution:
    def generateMatrix(self, n: int) -> list[list[int]]:
        if n == 1:
            return [[1]]
        if n == 2:
            return [[1, 2], [4, 3]]

        matrix = [[0 for _ in range(n)] for _ in range(n)]
        num = 1

        top_row, bottom_row, left_col, right_col = -1, n, -1, n
        while True:
            # print(f"started a new loop at top_row, bottom_row, left_col, right_col = {(top_row, bottom_row, left_col, right_col)}")
            # top-row
            i = top_row + 1
            for j in range(left_col + 1, right_col):
                matrix[i][j] = num
                num += 1
            top_row += 1
            # print(f"after printing top-row: {ret}")
            if top_row + 1 > bottom_row - 1:
                break

            j = right_col - 1
            for i in range(top_row + 1, bottom_row):
                matrix[i][j] = num
                num += 1
            right_col -= 1
            # print(f"after printing right-col: {ret}")
            if left_col + 1 > right_col - 1:
                break

            i = bottom_row - 1
            for j in range(right_col - 1, left_col, -1):
                matrix[i][j] = num
                num += 1
            bottom_row -= 1
            # print(f"after printing bottom-row: {ret}")
            if top_row + 1 > bottom_row - 1:
                break

            j = left_col + 1
            for i in range(bottom_row - 1, top_row, -1):
                matrix[i][j] = num
                num += 1
            left_col += 1
            # print(f"after printing leftright-col: {ret}")
            if left_col + 1 > right_col - 1:
                break

        return matrix


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(expected: list[list[int]], n: int) -> tuple[bool, str]:
    actual = Solution().generateMatrix(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                n=3,
                expected=[[1, 2, 3], [8, 9, 4], [7, 6, 5]],
            )
            Test(
                n=1,
                expected=[[1]],
            )
            Test(
                n=8,
                expected=[
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [28, 29, 30, 31, 32, 33, 34, 9],
                    [27, 48, 49, 50, 51, 52, 35, 10],
                    [26, 47, 60, 61, 62, 53, 36, 11],
                    [25, 46, 59, 64, 63, 54, 37, 12],
                    [24, 45, 58, 57, 56, 55, 38, 13],
                    [23, 44, 43, 42, 41, 40, 39, 14],
                    [22, 21, 20, 19, 18, 17, 16, 15],
                ],
            )
            Test(
                n=9,
                expected=[
                    [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    [32, 33, 34, 35, 36, 37, 38, 39, 10],
                    [31, 56, 57, 58, 59, 60, 61, 40, 11],
                    [30, 55, 72, 73, 74, 75, 62, 41, 12],
                    [29, 54, 71, 80, 81, 76, 63, 42, 13],
                    [28, 53, 70, 79, 78, 77, 64, 43, 14],
                    [27, 52, 69, 68, 67, 66, 65, 44, 15],
                    [26, 51, 50, 49, 48, 47, 46, 45, 16],
                    [25, 24, 23, 22, 21, 20, 19, 18, 17],
                ],
            )
            Test(
                n=2,
                expected=[[1, 2], [4, 3]],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
