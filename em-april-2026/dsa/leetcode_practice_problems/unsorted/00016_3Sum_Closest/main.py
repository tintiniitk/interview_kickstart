class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        min_diff = 10**9
        sum_min_diff = -(10**9)
        for i in range(n - 2):
            val = nums[i]
            start = i + 1
            end = n - 1
            while end > start:
                sum_val = val + nums[start] + nums[end]
                if abs(sum_val - target) < min_diff:
                    min_diff = abs(sum_val - target)
                    sum_min_diff = sum_val
                    if min_diff == 0:
                        return target
                if sum_val > target:
                    end -= 1
                else:  # sum_val < target
                    start += 1
        return sum_min_diff


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], target: int, expected: int) -> tuple[bool, str]:
    actual = Solution().threeSumClosest(nums, target)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[-1, 2, 1, -4], target=1, expected=2)
            Test(nums=[0, 0, 0], target=1, expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
