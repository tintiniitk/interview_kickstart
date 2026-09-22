from functools import cache


class Solution:
    def minDays(self, n: int) -> int:
        # streak_sum_to_streak_size = [-1 for _ in range(n + 1)]
        # streak_sum_to_streak_size[0] = 0
        streak_sum_to_streak_size = {0: 0}
        i = 1
        prev_streak_sum = 0
        while True:
            streak_sum = prev_streak_sum + i
            if streak_sum > n:
                break
            streak_sum_to_streak_size[streak_sum] = i
            prev_streak_sum = streak_sum
            i += 1
        # dp = streak_sum_to_streak_size
        # for s in range(2, n + 1):
        #     if dp[s] == -1:
        #         min_dp_s = s + 1
        #         for t in range(s - 1, s // 2 - 1, -1):
        #             min_dp_s = min(min_dp_s, dp[t] + 1 + dp[s - t])
        #         dp[s] = min_dp_s
        dp = [-1 for _ in range(n + 1)]
        dp[0] = 0
        dp[1] = 1
        for s in range(2, n + 1):
            if s not in streak_sum_to_streak_size:
                for t in range(s - 1, s // 2 - 1, -1):
                    if t in streak_sum_to_streak_size:
                        dp[s] = streak_sum_to_streak_size[t] + 1 + dp[s - t]
                        break
            else:
                dp[s] = streak_sum_to_streak_size[s]
        return dp[n]

        @cache
        def min_days(s: int) -> int:
            if dp[s] != -1:
                return dp[s]
            else:
                min_dp_s = 2 * s
                for t in range(s - 1, (s - 1) // 2, -1):
                    min_dp_s = min(min_dp_s, min_days(t) + 1 + min_days(s - t))
                if min_dp_s >= 2 * s:
                    raise ValueError(f"could not find min_days for s = {s}")
                return min_dp_s

        return min_days(n)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=5, stop_on_tc_failure=False)
def Test(n: int, expected: int) -> tuple[bool, str]:
    actual = Solution().minDays(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    sys.setrecursionlimit(5000)
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=1951, expected=77)
            Test(n=100000, expected=481)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
