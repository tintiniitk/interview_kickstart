class Solution:
    def isPossibleToRearrange(self, s: str, t: str, k: int) -> bool:
        n = len(s)
        # assert len(t) == n
        # assert n % k == 0
        # find size of each of the k substrings.
        r = n // k
        # find the frequency/count of each substring in s.
        freq = {}
        for i in range(0, n, r):
            substr = s[i : i + r]
            if substr in freq:
                freq[substr] += 1
            else:
                freq[substr] = 1
        # print(f"freq = {freq}")
        # for each substring s in t, either subtract it from freq, or return false if not present.
        for i in range(0, n, r):
            substr = t[i : i + r]
            if substr not in freq:
                return False
            freq[substr] -= 1
            if freq[substr] == 0:
                del freq[substr]
        return True


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, t: str, k: int, expected: bool) -> tuple[bool, str]:
    actual = Solution().isPossibleToRearrange(s, t, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="abcd", t="cdab", k=2, expected=True)
            Test(s="aabbcc", t="bbaacc", k=3, expected=True)
            Test(s="aabbcc", t="bbaacc", k=2, expected=False)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
