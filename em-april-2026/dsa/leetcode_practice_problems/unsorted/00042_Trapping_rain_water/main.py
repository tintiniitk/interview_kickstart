from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
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


def Test(height: List[int], expected: int):
    print(f"[RUN] Test case [height={height}, expected={expected}]")
    actual = Solution().trap(height)
    assert actual == expected, f"[FAILED]\nactual(={actual})"
    print(f"[DONE]")


Test([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6)
Test([4, 2, 0, 3, 2, 5], 9)
Test([1, 1, 1], 0)
Test([1, 0, 1], 1)
Test([1, 2, 1], 0)
Test([1, 2, 1, 2], 1)
