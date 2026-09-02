from collections import Counter


class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        counter = Counter(nums)
        unique_nums = set(nums)
        unique_nums_sorted = list(unique_nums)
        n = len(unique_nums_sorted)
        ret = []
        slate = []

        def helper(index: int):
            if index == n:
                ret.append(slate.copy())
                return
            num = unique_nums_sorted[index]
            freq = counter[num]
            helper(index + 1)
            for k in range(1, freq + 1):
                slate.append(num)
                helper(index + 1)
            for _ in range(freq):
                slate.pop()

        helper(0)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().subsetsWithDup(nums)
    if len(set(map(tuple, actual))) != len(actual):
        return False, f"Otput {truncate_param(actual)} has duplicates in it"
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 2, 2], expected=[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
            Test(nums=[0], expected=[[], [0]])
            Test(
                nums=[4, 4, 4, 1, 4],
                expected=[
                    [],
                    [1],
                    [1, 4],
                    [1, 4, 4],
                    [1, 4, 4, 4],
                    [1, 4, 4, 4, 4],
                    [4],
                    [4, 4],
                    [4, 4, 4],
                    [4, 4, 4, 4],
                ],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
