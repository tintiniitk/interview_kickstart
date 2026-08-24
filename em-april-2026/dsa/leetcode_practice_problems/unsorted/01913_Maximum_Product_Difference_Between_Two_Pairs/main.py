class Solution:
    def maxProductDifference(self, nums: list[int]) -> int:
        min_index, max_index = nums.index(min(nums)), nums.index(max(nums))
        min_index2, max_index2 = (
            nums.index(min(nums[:min_index] + nums[min_index + 1 :])),
            nums.index(max(nums[:max_index] + nums[max_index + 1 :])),
        )
        return nums[max_index2] * nums[max_index] - nums[min_index2] * nums[min_index]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maxProductDifference(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[5, 6, 2, 7, 4], expected=34)
            Test(nums=[4, 2, 5, 9, 7, 4, 8], expected=64)
            Test(nums=[1, 6, 7, 5, 2, 4, 10, 6, 4], expected=68)
            Test(nums=[8, 3, 5, 7], expected=41)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
