from functools import cache

MOD_BASE = 10**9 + 7


class Solution:
    def minNonZeroProduct(self, p: int) -> int:
        max_num = (1 << p) - 1
        num_pairs = max_num // 2  # power
        max_even = (max_num - 1) % MOD_BASE
        # we need to return ((max_even^num_pairs)*max_num)%MOD_BASE

        @cache
        def power(x: int) -> int:
            if x <= 0:
                return 1
            elif x == 1:
                return max_even
            half = x // 2
            if x % 2 == 0:
                return (power(half) * power(half)) % MOD_BASE
            return (max_even * ((power(half) * power(half)) % MOD_BASE)) % MOD_BASE

        return (power(num_pairs) * max_num) % MOD_BASE


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(p: int, expected: int) -> tuple[bool, str]:
    actual = Solution().minNonZeroProduct(p)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(p=1, expected=1)
            Test(p=2, expected=6)
            Test(p=3, expected=1512)
            Test(p=60, expected=813987236)
            Test(p=6, expected=57405498)
            Test(p=5, expected=202795991)
            Test(p=4, expected=581202553)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
