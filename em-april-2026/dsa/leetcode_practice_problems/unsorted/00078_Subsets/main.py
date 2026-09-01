class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        ret = []
        slate = []

        def helper(index: int):
            if index == n:
                ret.append(slate.copy())
                return
            # exclude
            helper(index + 1)
            # include
            slate.append(nums[index])
            helper(index + 1)
            slate.pop()

        helper(0)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().subsets(nums)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                nums=[1, 2, 3],
                expected=[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]],
            )
            Test(nums=[0], expected=[[], [0]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
