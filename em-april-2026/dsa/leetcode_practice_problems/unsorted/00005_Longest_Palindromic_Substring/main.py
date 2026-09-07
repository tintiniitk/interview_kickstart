class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return None
        n = len(s)
        res = s[:1]
        if n == 1:
            return "".join(res)
        maxl = 1
        # odd substrings
        for i in range(1, n - 1):
            l, r = i - 1, i + 1
            while 0 <= l and r <= n - 1 and s[l] == s[r]:
                if r - l + 1 > maxl:
                    maxl = r - l + 1
                    res = s[l : r + 1]
                l -= 1
                r += 1
        # even substrings
        for i in range(n - 1):
            l, r = i, i + 1
            while 0 <= l and r <= n - 1 and s[l] == s[r]:
                if r - l + 1 > maxl:
                    maxl = r - l + 1
                    res = s[l : r + 1]
                l -= 1
                r += 1
        return "".join(res)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: str) -> tuple[bool, str]:
    actual = Solution().longestPalindrome(s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="babad", expected="bab")
            Test(s="cbbd", expected="bb")
            Test(s="a", expected="a")
            Test(s="bb", expected="bb")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
