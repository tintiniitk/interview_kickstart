class Solution:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        if m == 1 == n:
            return 1 if matrix[0][0] == "1" else 0
        matrix_int = [list(map(int, row)) for row in matrix]
        for i in range(m):
            for j in range(n):
                if j > 0 and matrix_int[i][j] == 1:
                    matrix_int[i][j] += matrix_int[i][j - 1]
        global_max_area = 0
        for j in range(n):
            for i in range(m):
                if matrix_int[i][j] > 0:
                    max_width = matrix_int[i][j]
                    global_max_area = max(max_width, global_max_area)
                    k = i + 1
                    while k < m:
                        max_width = min(max_width, matrix_int[k][j])
                        if max_width == 0:
                            break
                        global_max_area = max(global_max_area, max_width * (k - i + 1))
                        k += 1
        return global_max_area


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(matrix: list[list[str]], expected: int) -> tuple[bool, str]:
    actual = Solution().maximalRectangle(matrix)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                matrix=[
                    ["1", "0", "1", "0", "0"],
                    ["1", "0", "1", "1", "1"],
                    ["1", "1", "1", "1", "1"],
                    ["1", "0", "0", "1", "0"],
                ],
                expected=6,
            )
            Test(matrix=[["0"]], expected=0)
            Test(matrix=[["1"]], expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
