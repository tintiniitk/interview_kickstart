class Solution:
    def minDays(self, n: int) -> int:
        streak_sum_to_streak_size = {0: 0}
        i = 1
        prev_streak_sum = 0
        streak_sums = []
        while True:
            streak_sum = prev_streak_sum + i
            if streak_sum > n:
                break
            streak_sum_to_streak_size[streak_sum] = i
            streak_sums.append(streak_sum)
            prev_streak_sum = streak_sum
            i += 1

        dp = [-1 for _ in range(n + 1)]
        dp[0] = 0
        dp[1] = 1
        for s in range(2, n + 1):
            if s not in streak_sums:
                min_dp_s = 2 * s
                for streak_sum in streak_sums:
                    if streak_sum >= s:
                        break
                    min_dp_s = min(
                        min_dp_s,
                        streak_sum_to_streak_size[streak_sum] + 1 + dp[s - streak_sum],
                    )
                dp[s] = min_dp_s
            else:
                dp[s] = streak_sum_to_streak_size[s]
        return dp[n]


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
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=2, expected=3)
            Test(n=9, expected=6)
            Test(n=12, expected=7)
            Test(n=1951, expected=77)
            Test(n=100000, expected=481)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
