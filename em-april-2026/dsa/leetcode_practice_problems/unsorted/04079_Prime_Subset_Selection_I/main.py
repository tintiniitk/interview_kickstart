from math import sqrt


class Solution:
    def maxPrimes(self, n: int, s: int) -> list[int]:
        if s < 2 or n < 2:
            return []
        is_composite = [False] * (n + 1)
        is_composite[2] = True
        sqrt_n = int(sqrt(n))
        ss = 2
        ret = [2]
        for i in range(2, 1 + n // 2, 1):
            is_composite[2 * i] = True
        for i in range(3, n + 1, 2):
            if i % 2 == 1 and not is_composite[i]:
                if ss + i <= s:
                    ret.append(i)
                    ss += i
                if i <= sqrt_n:
                    for j in range(i, 1 + n // i, 2):
                        k = i * j
                        is_composite[k] = True
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, s: int, expected: set[tuple[int]]) -> tuple[bool, str]:
    actual = Solution().maxPrimes(n, s)
    if tuple(actual) not in expected:
        return False, f"got={actual} not in wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=11, s=849, expected=[(2, 3, 5, 7, 11)])
            Test(n=5, s=5, expected=[(2, 3)])
            Test(n=1, s=3, expected=[()])
            Test(n=7, s=20, expected=[(2, 3, 5, 7)])
            Test(n=15, s=15, expected=[(2, 3, 5), (2, 3, 7), (2, 5, 7)])
            Test(n=5, s=1, expected=[()])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
