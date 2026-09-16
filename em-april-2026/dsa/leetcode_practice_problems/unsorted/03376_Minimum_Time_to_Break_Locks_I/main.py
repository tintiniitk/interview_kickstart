from functools import cache


class Solution:
    def findMinimumTime(self, strength: list[int], k: int) -> int:
        @cache
        def min_time_remaining(remaining_locks: tuple[int], cur_factor: int) -> int:
            if not remaining_locks:
                return 0
            if len(remaining_locks) == 1:
                return ceil(strength[remaining_locks[0]] / cur_factor)
            return min(
                ceil(strength[remaining_locks[index]] / cur_factor)
                + min_time_remaining(
                    tuple(remaining_locks[:index] + remaining_locks[index + 1 :]),
                    cur_factor + k,
                )
                for index in range(len(remaining_locks))
            )

        return min_time_remaining(tuple(range(len(strength))), 1)


import sys
from math import ceil

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(strength: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().findMinimumTime(strength, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(strength=[3, 4, 1], k=1, expected=4)
            Test(strength=[2, 5, 4], k=2, expected=5)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
