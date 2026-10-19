class Solution:
    def minDeletions(self, nums: list[int]) -> int:
        assert nums is not None
        n = len(nums)
        assert n >= 2
        count = 0
        prev = nums[0]
        for i in range(1, n):
            cur = nums[i]
            if cur == prev:
                count += 1
            else:
                prev = cur
        return count


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().minDeletions(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 1, 2, 2, 2, 3], expected=3)
            Test(nums=[4, 4, 9, 4], expected=1)
            Test(nums=[4, 4, 5, 6, 6, 7], expected=2)
            Test(nums=[4, 4, 5], expected=1)
            Test(nums=[4, 5, 6], expected=0)
            Test(nums=[4, 3], expected=0)
            Test(nums=[4, 4], expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
