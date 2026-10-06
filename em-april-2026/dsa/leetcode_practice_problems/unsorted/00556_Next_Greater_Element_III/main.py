class Solution:
    def nextGreaterElement(self, n: int) -> int:
        if n <= 11:
            return -1
        digits = list(map(int, str(n)))
        n = len(digits)
        # print(f"digits={digits}")
        # Based on the solution provided in https://leetcode.com/problems/next-greater-element-iii/solutions/983076/python-om-solution-explained-by-dbabiche-zlin.
        # Find first falling index i from the right, i.e. highest i such that digits[i] < digits[i+1] for 0 < = i < n-1. It's guaranteed that the digits[i+1]...digits[n-1] are in non-increasing order.
        i = n - 2
        while i >= 0:
            if digits[i] < digits[i + 1]:
                break
            i -= 1
        # print(f"i={i}")
        if (
            i <= -1
        ):  # i=-1 implies all digits are already in descending order, and there is no next greater number.
            return -1
        # Find smallest j such that i < j < n such that digits[j] > digits[i] >= digits[j+1], or if j = n-1 and digits[i] < digits[j].
        j = i + 1
        while j < n - 1:
            if digits[j] > digits[i] >= digits[j + 1]:
                break
            j += 1
        # print(f"j={j}")
        # There must be such a j.
        # assert i < j < n
        # assert digits[j] > digits[i]
        # assert j == n - 1 or digits[i] >= digits[j + 1]
        # Swap digits[i], digits[j]. This won't break the guarantee that digits[i+1]...digits[n-1] are in non-increasing order.
        digits[i], digits[j] = digits[j], digits[i]
        # Now, digits[i] has become higher than before, thus a higher number.
        # print(f"After swapping digits={digits}")
        # Now, reverse digits[i+1:] to make it non-decreasing to make the smallest number from digits[i+1:].
        # digits[i + 1 :] = digits[:i:-1]
        digits[i + 1 :].reverse()
        # Now, reassemble digits to make number and return.
        candidate = int("".join(map(str, digits)))
        return candidate if candidate < 2**31 else -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: int) -> tuple[bool, str]:
    actual = Solution().nextGreaterElement(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=12, expected=21)
            Test(n=21, expected=-1)
            Test(n=3, expected=-1)
            Test(n=101, expected=110)
            Test(n=2341, expected=2413)
            Test(n=4321, expected=-1)
            Test(n=4231, expected=4312)
            Test(n=1000, expected=-1)
            Test(n=230241, expected=230412)
            Test(n=2147483486, expected=-1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
