class Solution:
    def maximizeSum(self, nums: list[int], k: int) -> int:
        def max_variation(num: int) -> int:
            return int("".join(sorted(str(num), reverse=True)))

        orig_sum = sum(nums)
        diffs = [max_variation(num) - num for num in nums]
        diffs.sort(reverse=True)
        return orig_sum + sum(diffs[:k])


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().maximizeSum(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[123, 45], k=1, expected=366)
            Test(nums=[102, 90, 14], k=2, expected=341)
            # Test(nums=      ,k =          , expected=   )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
