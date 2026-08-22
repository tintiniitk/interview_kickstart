from itertools import permutations


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        return [list(permutation) for permutation in permutations(nums, len(nums))]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


def compare_permutations(
    list1: list[list[int]], list2: list[list[int]]
) -> tuple[bool, str]:
    if list1 and not list2:
        return False, "set1 and not set2"
    if list2 and not list1:
        return False, "set2 and not set1"
    if len(list1) != len(list2):
        return False, "len(set1) != len(set2)"
    set1 = {tuple(item) for item in list1}
    if len(set1) != len(list1):
        return False, "list1 has duplicates"
    set2 = {tuple(item) for item in list2}
    if len(set2) != len(list2):
        return False, "list2 has duplicates"
    if set1 != set2:
        return False, "list1 != list2"
    return True, ""


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().permute(nums)
    return compare_permutations(actual, expected)


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                nums=[1, 2, 3],
                expected=[
                    [1, 2, 3],
                    [1, 3, 2],
                    [2, 1, 3],
                    [2, 3, 1],
                    [3, 1, 2],
                    [3, 2, 1],
                ],
            )
            Test(nums=[0, 1], expected=[[0, 1], [1, 0]])
            Test(nums=[1], expected=[[1]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
