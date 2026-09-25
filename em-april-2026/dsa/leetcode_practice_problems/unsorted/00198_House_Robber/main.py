class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [0 for _ in range(n + 1)]
        dp[1] = nums[0]
        for i in range(2, n + 1):
            dp[i] = max(dp[i - 1], nums[i - 1] + dp[i - 2])
        return max(dp[n], dp[n - 1])


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().rob(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 2, 3, 1], expected=4)
            Test(nums=[2, 7, 9, 3, 1], expected=12)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
