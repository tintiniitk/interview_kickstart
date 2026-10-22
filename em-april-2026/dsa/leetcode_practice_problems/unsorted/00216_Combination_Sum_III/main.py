class Solution:
    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        # output combinations
        combinations = []
        # intermittent current combination
        slate = [0] * k

        def helper(next_num: int, l: int, s: int):
            """run future iteration(s) starting with next_num to be included or not, a slate of current count l, and current sum s.

            Args:
                next_num (int): next number to be included or skipped.
                l (int): number of the elements in the slate currently. When it's k, then slate is full.
                s (int): sum of the elements in the slate currently. When it l is k, and s is n, then slate is a valid combination.
            """
            if l == k:
                if s == n:
                    combinations.append(slate.copy())
                return
            if s >= n:
                return
            if next_num > 9:
                return
            # Try including next number.
            slate[l] = next_num
            helper(next_num + 1, l + 1, s + next_num)
            # Try excluding next number.
            helper(next_num + 1, l, s)

        # First iteration starting with next-number 1, with empty slate.
        helper(1, 0, 0)
        # return all the output combinations formed by the above helper call.
        return combinations


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(k: int, n: int, expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().combinationSum3(k, n)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(k=3, n=7, expected=[[1, 2, 4]])
            Test(k=3, n=9, expected=[[1, 2, 6], [1, 3, 5], [2, 3, 4]])
            Test(k=4, n=1, expected=[])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
