class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        # Modified O(n) approach
        nums2_rev_map = {num: i for i, num in enumerate(nums2)}
        n = len(nums2)
        stack = []
        next_greater_numbers = [-1] * n
        for i in range(n - 2, -1, -1):
            prev = nums2[i + 1]
            cur = nums2[i]
            if prev > cur:
                stack.append(prev)
                next_greater_numbers[i] = prev
            else:
                while stack and stack[-1] <= cur:
                    stack.pop()
                if stack:
                    next_greater_numbers[i] = stack[-1]
        return [next_greater_numbers[nums2_rev_map[num]] for num in nums1]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums1: list[int], nums2: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = Solution().nextGreaterElement(nums1, nums2)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums1=[4, 1, 2], nums2=[1, 3, 4, 2], expected=[-1, 3, -1])
            Test(nums1=[2, 4], nums2=[1, 2, 3, 4], expected=[3, -1])
            Test(
                nums1=[1, 3, 5, 2, 4],
                nums2=[6, 5, 4, 3, 2, 1, 7],
                expected=[7, 7, 7, 7, 7],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
