EPSILON = 10**-12


class Solution:
    def myPow(self, x: float, n: int) -> float:
        if x == 0:
            return 0
        if x == 1:
            return 1
        if x == -1:
            return -1 if n % 2 else 1

        def pow_internal(n: int) -> float:
            if n == 0:
                return 1
            if n == 1:
                return x
            if n == -1:
                return 1 / x
            half = n // 2
            if n % 2:
                return x * pow_internal(half) ** 2
            else:
                return pow_internal(half) ** 2

        return pow_internal(n)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(x: float, n: int, expected: float) -> tuple[bool, str]:
    actual = Solution().myPow(x, n)
    if abs(actual - expected) > EPSILON:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(x=2.0, n=10, expected=1024.0)
            Test(x=2.1, n=3, expected=9.261)
            Test(x=2.0, n=-2, expected=0.25)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
