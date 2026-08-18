from functools import cache


class Solution:
    def checkValidString(self, s: str) -> bool:
        n = len(s)
        n_by_2 = (n + 1) // 2

        # # Without cache, idea works but runs out of time (TLE) because number of branches is 3^n in worst case.
        # # TC = SC = O(n^2)
        # @cache
        # def dp_helper(index: int, depth: int) -> bool:
        #     if index == n:
        #         return depth == 0
        #     c = s[index]
        #     if c == "*":
        #         # try (  for * or # try ) for * or # try '' for *
        #         return (
        #             (depth <= n_by_2 and dp_helper(index + 1, depth + 1))
        #             or (depth > 0 and dp_helper(index + 1, depth - 1))
        #             or (dp_helper(index + 1, depth))
        #         )
        #     elif c == "(":
        #         if depth > n_by_2:
        #             return False
        #         return dp_helper(index + 1, depth + 1)
        #     elif c == ")":
        #         if depth <= 0:
        #             return False
        #         return dp_helper(index + 1, depth - 1)
        #     else:
        #         raise ValueError(
        #             f"Encountered unexpected character {c} in input strin {s}"
        #         )
        #     return True
        # return dp_helper(0, 0)

        # TC = O(n), SC=O(1)
        openCount, closeCount = 0, 0
        for i in range(n):
            c1, c2 = s[i], s[n - 1 - i]
            if c1 in {"(", "*"}:
                openCount += 1
            else:
                openCount -= 1
            if openCount < 0:
                return False
            if c2 in {")", "*"}:
                closeCount += 1
            else:
                closeCount -= 1
            if closeCount < 0:
                return False
        return True


from utils.pretty_test_runner import pretty_test_runner, truncate_param
from utils.context_manager import time_limit, TimeoutException


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: bool) -> (bool, str):
    actual = Solution().checkValidString(s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print(f"Running tests ...")
        with time_limit(5):
            Test(s="()", expected=True)
            Test(s="(*)", expected=True)
            Test(s="(*))", expected=True)
            Test(s="(()", expected=False)
            Test(s="())", expected=False)
            Test(s="*))", expected=False)
            Test(s="((*", expected=False)
            Test(s="(*(*", expected=True)
            Test(s="((**", expected=True)
            Test(s="", expected=True)
            Test(s="*", expected=True)
            Test(s="".join(["*"] * 100), expected=True)
            Test(s="".join(["(("] + ["*"] * 98), expected=True)
            Test(s="(" + "".join(["*"] * 99), expected=True)
            Test(s="(" + "".join(["*"] * 4), expected=True)
            Test(s="((" + "".join(["*"] * 4), expected=True)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
    except Exception as e:
        print(f"Tests failed: {e}")


if __name__ == "__main__":
    main()
