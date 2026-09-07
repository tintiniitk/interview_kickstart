class Solution:
    def partition(self, s: str) -> list[list[str]]:
        n = len(s)
        if n == 1:
            return [[s]]
        slate = []
        ret = []

        def is_palindromic(s1: list[str]) -> bool:
            return s1 == s1[::-1]

        def helper(index: int, was_latest_palindrome: bool):
            if index == n:
                if was_latest_palindrome:
                    ret.append(["".join(v) for v in slate])
                return
            c = s[index]
            # try and include c in the latest palindrome
            slate[-1].append(c)
            helper(index + 1, is_palindromic(slate[-1]))
            slate[-1].pop()
            # try and leave out c into a new palindrome
            if was_latest_palindrome:
                slate.append([c])
                helper(index + 1, True)
                slate.pop()

        slate = [[s[0]]]
        helper(1, True)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: list[list[str]]) -> tuple[bool, str]:
    actual = Solution().partition(s)
    if sorted(map(tuple, actual)) != sorted(map(tuple, expected)):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="aab", expected=[["a", "a", "b"], ["aa", "b"]])
            Test(s="a", expected=[["a"]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
