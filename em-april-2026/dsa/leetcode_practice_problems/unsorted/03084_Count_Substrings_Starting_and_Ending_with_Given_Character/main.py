class Solution:
    def countSubstrings(self, s: str, c: str) -> int:
        n = s.count(c)
        return (n * (n + 1)) // 2


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, c: str, expected: int) -> tuple[bool, str]:
    actual = Solution().countSubstrings(s, c)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="abada", c="a", expected=6)
            Test(s="zzz", c="z", expected=6)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
