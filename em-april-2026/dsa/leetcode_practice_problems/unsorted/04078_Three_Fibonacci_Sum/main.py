class Solution:
    def threeFibonacciSum(self, n: int) -> bool:
        if n < 2:
            return False
        prev2, prev = 0, 1
        while True:
            cur = prev2 + prev
            if 2 * cur >= n:
                if 2 * cur == n:
                    return True
                elif 2 * cur > n:
                    return False
            prev2, prev = prev, cur
        return False


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: bool) -> tuple[bool, str]:
    actual = Solution().threeFibonacciSum(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=16, expected=True)
            Test(n=2, expected=True)
            Test(n=3, expected=False)
            Test(n=15, expected=False)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
