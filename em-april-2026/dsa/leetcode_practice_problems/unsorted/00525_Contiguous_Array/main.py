class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        delta = 0
        max_len = 0
        min_index_for_delta = {0: -1}
        for i, num in enumerate(nums):
            delta += 1 if num == 0 else -1
            if delta in min_index_for_delta:
                max_len = max(max_len, i - min_index_for_delta[delta])
            else:
                min_index_for_delta[delta] = i
        return max_len


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().findMaxLength(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[0, 1], expected=2)
            Test(nums=[0, 1, 0], expected=2)
            Test(nums=[0, 1, 1, 1, 1, 1, 0, 0, 0], expected=6)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
