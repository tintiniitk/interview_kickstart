from functools import cache


class Solution:
    def numTrees(self, n: int) -> int:
        if n <= 2:
            return n
        # dp = [0 for i in range(n+1)]
        # dp[0] = 1
        # dp[1] = 1
        # dp[2] = 2
        # # level = 1
        # def num_unique_bst(k: int) -> int:
        #     # nonlocal level
        #     # print(f"{'  '*level}num_unique_bst({k})")
        #     # level += 1
        #     if dp[k] > 0:
        #         # level -= 1
        #         return dp[k]
        #     dp[k] = 0
        #     for root in range(1,k+1):
        #         dp[k] += num_unique_bst(root-1) * num_unique_bst(k-root)
        #     # level -= 1
        #     return dp[k]
        # return num_unique_bst(n)

        @cache
        def num_unique_bst(k: int) -> int:
            if k <= 1:
                return 1
            if k == 2:
                return 2
            return sum(
                num_unique_bst(root - 1) * num_unique_bst(k - root)
                for root in range(1, k + 1)
            )

        return num_unique_bst(n)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: int) -> tuple[bool, str]:
    actual = Solution().numTrees(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=3, expected=5)
            Test(n=1, expected=1)
            Test(n=4, expected=14)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
