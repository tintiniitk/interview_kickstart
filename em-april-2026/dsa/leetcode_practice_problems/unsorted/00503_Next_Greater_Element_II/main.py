class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        n = len(nums)
        if n == 1:
            return [-1]

        stack = []
        # pre-insert elements [n-2,...,0] (only fill stack) to prepare the array before processing it for [n-1...0] in a second pass.
        for i in range(n - 2, -1, -1):
            prev = nums[i + 1]
            cur = nums[i]
            if prev > cur:
                stack.append(prev)
            else:
                while stack and stack[-1] <= cur:
                    stack.pop()

        next_greater_numbers = [-1] * n
        for i in range(n - 1, -1, -1):
            prev = nums[(i + 1) % n]
            cur = nums[i]
            if prev > cur:
                stack.append(prev)
                next_greater_numbers[i] = prev
            else:
                while stack and stack[-1] <= cur:
                    stack.pop()
                if stack:
                    next_greater_numbers[i] = stack[-1]
        return next_greater_numbers


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = Solution().nextGreaterElements(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1], expected=[-1])
            Test(
                nums=[
                    4,
                    4,
                    4,
                ],
                expected=[-1, -1, -1],
            )
            Test(nums=[4, -4, 4, -4, 4, -4], expected=[-1, 4, -1, 4, -1, 4])
            Test(nums=[1, 2, 1], expected=[2, -1, 2])
            Test(nums=[1, 2, 3, 4, 3], expected=[2, 3, 4, -1, 4])
            Test(nums=[4, 5, 3, 1, 2], expected=[5, -1, 4, 2, 4])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
