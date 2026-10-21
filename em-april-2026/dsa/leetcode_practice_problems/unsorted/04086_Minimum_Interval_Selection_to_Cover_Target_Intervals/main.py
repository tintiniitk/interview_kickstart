class Solution:
    def minSelection(
        self, availableIntervals: list[list[int]], targetIntervals: list[list[int]]
    ) -> int:
        return -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    availableIntervals: list[list[int]], targetIntervals: list[list[int]], expected: int
) -> tuple[bool, str]:
    actual = Solution().minSelection(availableIntervals, targetIntervals)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                availableIntervals=[[1, 4], [1, 7], [3, 9], [5, 10], [10, 15]],
                targetIntervals=[[1, 3], [2, 5], [7, 8], [10, 13], [11, 15], [12, 13]],
                expected=3,
            )
            Test(
                availableIntervals=[[4, 6], [1, 4], [2, 5]],
                targetIntervals=[[3, 4], [2, 5], [6, 7]],
                expected=-1,
            )
            Test(
                availableIntervals=[[1, 2], [3, 4]],
                targetIntervals=[[1, 4]],
                expected=-1,
            )
            # Test(availableIntervals=        , targetIntervals=           , expected=        )
            # Test(availableIntervals=        , targetIntervals=           , expected=        )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
