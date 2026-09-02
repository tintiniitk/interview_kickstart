from functools import cache


class Solution:
    def minimumTotal(self, triangle: list[list[int]]) -> int:
        n = len(triangle)
        if n == 1:
            return triangle[0][0]

        @cache
        def minimum(row: int, col: int) -> int:
            if row == n - 1:
                return triangle[n - 1][col]
            return triangle[row][col] + min(
                minimum(row + 1, col), minimum(row + 1, col + 1)
            )

        return minimum(0, 0)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(triangle: list[list[int]], expected: int) -> tuple[bool, str]:
    actual = Solution().minimumTotal(triangle)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(triangle=[[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]], expected=11)
            Test(triangle=[[-10]], expected=-10)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
