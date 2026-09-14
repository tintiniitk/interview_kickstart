from collections import defaultdict


class Solution:
    def shadowPairs(self, nums: list[int]) -> int:
        n = len(nums)
        count = 0
        stack = [nums[0]]
        stack_freq = defaultdict(int)
        stack_freq[nums[0]] = 1
        for i in range(1, n):
            new_num = nums[i]
            # remove all numbers in stack which are above new_num.
            while stack and stack[-1] > new_num:
                stack_freq[stack[-1]] -= 1
                if stack_freq[stack[-1]] == 0:
                    del stack_freq[stack[-1]]
                stack.pop()
            # account all numbers in stack which are < new_num.
            if stack:
                count += len(stack)
                if stack[-1] == new_num and new_num in stack_freq:
                    count -= stack_freq[new_num]
            # append the new num in the stack.
            assert not stack or stack[-1] <= new_num
            stack.append(new_num)
            stack_freq[new_num] += 1
        return count


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().shadowPairs(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc
from tc_y import tc as tc_y_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[3, 1, 4, 1, 5], expected=3)
            Test(nums=[6, 7, 6, 6, 7], expected=4)
            Test(nums=[1, 2, 3, 4], expected=6)
            Test(nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], expected=45)
            Test(**tc_x_tc)
            Test(**tc_y_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
