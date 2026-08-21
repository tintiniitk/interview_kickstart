class Solution:
    def trap(self, height: list[int]) -> int:
        n = len(height)
        # # original solution I came up with which costs TC=O(n), SC=O(n)
        # maxes_after = [0]
        # for j in range(n - 2, -1, -1):
        #     maxes_after.append(max(maxes_after[-1], height[j + 1]))
        # maxes_after.reverse()
        # max_before = 0
        # ret = 0
        # for i in range(1, n - 1):
        #     max_before = max(max_before, height[i - 1])
        #     ret += max(0, min(max_before, maxes_after[i]) - height[i])
        # return ret
        # Optimal solution available on internet: TC=O(n), SC=O(1)
        l, r = 0, n - 1
        maxLeft, maxRight = height[l], height[r]
        water = 0
        while l < r:
            if maxLeft <= maxRight:
                l += 1
                maxLeft = max(maxLeft, height[l])
                water += maxLeft - height[l]
            else:
                r -= 1
                maxRight = max(maxRight, height[r])
                water += maxRight - height[r]
        return water


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(height: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().trap(height)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


try:
    with time_limit(5):
        Test([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6)
        Test([4, 2, 0, 3, 2, 5], 9)
        Test([1, 1, 1], 0)
        Test([1, 0, 1], 1)
        Test([1, 2, 1], 0)
        Test([1, 2, 1, 2], 1)
except TimeoutException as te:
    print(te)
    sys.exit(1)
