class Solution:
    def minCost(self, nums: list[int]) -> int:
        n = len(nums)
        ret = nums[0] + nums[-1]
        if n >= 4:
            nums = sorted(nums[1:-1])
            i = 0
            while i < n - 2 - 1:
                ls = nums[i] + nums[i + 1]
                if ls >= 0:
                    break
                ret += ls
                i += 2
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().minCost(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 2], expected=3)
            Test(nums=[1, 2, 3], expected=4)
            Test(nums=[2, -7, 3, -5], expected=-7)
            Test(nums=[4, 0, -5, 2], expected=1)
            Test(nums=[7, -8, 1], expected=8)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
