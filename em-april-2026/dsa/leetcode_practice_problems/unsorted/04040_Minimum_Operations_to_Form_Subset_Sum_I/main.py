class Solution:
    def minOperations(self, nums: list[int], sum: int) -> int:
        def find_variations(num: int) -> list[tuple[int, int]]:
            ret = [(num, 0)]
            ops = 1
            cur = num // 2
            while cur > 0:
                ret.append((cur, ops))
                cur = cur // 2
                ops += 1
            ops = 1
            cur = num * 2
            while cur <= sum:
                ret.append((cur, ops))
                cur = cur * 2
                ops += 1
            return ret

        variations = {num: find_variations(num) for num in set(nums)}
        n = len(nums)
        dp = [[-1 for _ in range(1 + sum)] for _ in range(n + 1)]
        # dp[i][j] = smallest number of operations for sum j from subsets of nums[:i+1]
        # dp[0][1...sum] are all -1 because sum can't be created just from 0.
        # dp[1..n][0] are all 0 because sum can't be created just from 0.
        for i in range(n + 1):
            dp[i][0] = 0
        for i in range(1, n + 1):
            num = nums[i - 1]
            dp[i][:] = dp[i - 1][:]
            for j in range(1, sum + 1):
                for variation, ops in variations[num]:
                    if variation <= j and dp[i - 1][j - variation] >= 0:
                        if dp[i][j] > -1:
                            dp[i][j] = min(dp[i][j], dp[i - 1][j - variation] + ops)
                        else:
                            dp[i][j] = dp[i - 1][j - variation] + ops
        return dp[n][sum]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], sum: int, expected: int) -> tuple[bool, str]:
    actual = Solution().minOperations(nums, sum)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[5, 6, 10], sum=4, expected=3)
            Test(nums=[10, 2], sum=13, expected=3)
            Test(nums=[6, 3], sum=8, expected=-1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
