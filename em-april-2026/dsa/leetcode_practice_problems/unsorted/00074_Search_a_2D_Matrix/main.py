class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])
        N = m * n - 1

        def index2ij(index: int) -> tuple[int, int]:
            return (index // n, index % n)

        def ij2index(i: int, j: int) -> int:
            return i * n + j

        def find_target(start: int, end: int) -> bool:
            if end < start or start > N or end < 0:
                return False
            mid = (start + end) // 2
            i, j = index2ij(mid)
            mid_val = matrix[i][j]
            if mid_val == target:
                return True
            elif mid_val > target:
                return find_target(start, mid - 1)
            else:
                return find_target(mid + 1, end)

        return find_target(0, N)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(matrix: list[list[int]], target: int, expected: bool) -> tuple[bool, str]:
    actual = Solution().searchMatrix(matrix, target)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                matrix=[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
                target=3,
                expected=True,
            )
            Test(
                matrix=[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
                target=13,
                expected=False,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
