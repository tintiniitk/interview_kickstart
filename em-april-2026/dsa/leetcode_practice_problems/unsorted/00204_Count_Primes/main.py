from math import sqrt

composites = [False] * (5 * 10**6 + 1)


def mark_composites(k: int):
    if composites[k]:
        return False
    sqrt_k = int(sqrt(k))
    for i in range(2, sqrt_k + 1):
        if composites[i]:
            continue
        for j in range(i, k // i + 1):
            composites[i * j] = True


class Solution:
    def countPrimes(self, n: int) -> int:
        if n < 2:
            return 0
        mark_composites(n)
        return n - 2 - sum(composites[2:n])


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1.5, stop_on_tc_failure=False)
def Test(n: int, expected: int) -> tuple[bool, str]:
    actual = Solution().countPrimes(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from time import perf_counter

from utils.time import format_minimal_seconds


def main():
    try:
        print("Running tests ...")
        start = perf_counter()
        with time_limit(5):
            Test(n=10, expected=4)
            Test(n=0, expected=0)
            Test(n=1, expected=0)
            Test(n=100, expected=25)
            Test(n=1000, expected=168)
            Test(n=100000, expected=9592)
            Test(n=4999999, expected=348512)
            # Test(n=4649862, expected=325697)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)
    finally:
        end = perf_counter()
        print(f"Run of all tests took {format_minimal_seconds(end - start)}")


if __name__ == "__main__":
    main()
