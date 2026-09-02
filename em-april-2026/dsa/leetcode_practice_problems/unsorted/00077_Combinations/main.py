from itertools import combinations


class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        return list(map(list, combinations(list(range(1, n + 1)), k)))


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().combine(n, k)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=4, k=2, expected=[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])
            Test(n=1, k=1, expected=[[1]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
