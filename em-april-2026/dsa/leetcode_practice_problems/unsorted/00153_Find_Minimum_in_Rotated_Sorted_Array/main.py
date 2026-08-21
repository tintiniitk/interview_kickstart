class Solution:
    def findMin(self, nums: list[int]) -> int:
        n = len(nums)
        print(f"nums={nums}")

        def find_max_index(start: int, end: int) -> int:
            # print(f"find_max_index({start},{end})")
            size = end - start
            if size == 1:
                return start
            if size == 2:
                if nums[start] >= nums[end - 1]:
                    return start
                else:
                    return end - 1
            mid = (start + end) // 2
            if nums[start] <= nums[end - 1]:
                return end - 1
            elif nums[mid] >= nums[start]:
                return find_max_index(mid, end)
            else:  # nums[mid] < nums[start]:
                return find_max_index(start, mid)
            return -1

        max_index = find_max_index(0, n)
        # print(f"max_index={max_index}")
        if max_index == -1:
            raise ValueError("max_index == -1")
        return nums[(max_index + 1) % n]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().findMin(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[3, 4, 5, 1, 2], expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
