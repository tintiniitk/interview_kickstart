from functools import cmp_to_key


def custom_cmp(s1: str, s2: str) -> int:
    if s1 == s2:
        return 0

    def basic_cmp():
        return -1 if s1 < s2 else 1

    l1 = len(s1)
    l2 = len(s2)
    if l1 == l2:
        return basic_cmp()
    if l1 > l2:
        if s1.startswith(s2):
            return custom_cmp(s1[l2:], s2)
        return basic_cmp()
    if s2.startswith(s1):
        return custom_cmp(s1, s2[l1:])
    return basic_cmp()


class Solution:
    def largestNumber(self, nums: list[int]) -> str:
        if all(num == 0 for num in nums):
            return "0"
        num_strings = list(map(str, nums))
        num_strings.sort(key=cmp_to_key(custom_cmp), reverse=True)
        # print(f"sorted num_strings = {num_strings}")
        return "".join(num_strings)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: str) -> tuple[bool, str]:
    actual = Solution().largestNumber(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[10, 2], expected="210")
            Test(nums=[3, 30, 34, 5, 9], expected="9534330")
            Test(
                nums=[
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    111,
                    100000000,
                    10000000,
                ],
                expected="1111111111111111110000000100000000",
            )
            Test(
                nums=[
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    111,
                    100000000,
                    10000000,
                    101010101,
                    10101010,
                ],
                expected="111111111111111111010101011010101010000000100000000",
            )
            Test(
                nums=[
                    1,
                    11,
                    111,
                    100000000,
                    10000000,
                    101010101,
                    10101010,
                ],
                expected="1111111010101011010101010000000100000000",
            )
            Test(nums=[0, 0], expected="0")
            Test(nums=[0, 0, 1], expected="100")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
