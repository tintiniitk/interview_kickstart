class Solution:
    def sortPermutation(self, nums: list[int]) -> int:
        k = 0
        first = True
        for i, num in enumerate(nums):
            if i != num:
                if first:
                    k = num
                    first = False
                else:
                    k &= num
        return k


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().sortPermutation(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[0, 3, 2, 1], expected=1)
            Test(nums=[0, 1, 3, 2], expected=2)
            Test(nums=[3, 2, 1, 0], expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
