class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        n = len(nums)
        if n < 4:
            return []
        if n == 4:
            if sum(nums) == target:
                return [nums]
            else:
                return []
        # print(f"nums={nums}")
        nums.sort()
        # print(f"sorted(nums)={nums}")

        # sub-optimal O(n^3) solution
        # ret = set()
        # for i in range(n-3):
        #     a = nums[i]
        #     for j in range(i+1, n-2):
        #         b = nums[j]
        #         rem_target = target - a - b
        #         start = j+1
        #         end = n-1
        #         while start < end:
        #             c = nums[start]
        #             d = nums[end]
        #             s = c + d
        #             if s == rem_target:
        #                 ret.add((a,b,c,d))
        #                 start += 1
        #                 end -=1
        #             elif s < rem_target:
        #                 start += 1
        #             else : # if s > rem_target
        #                 end -= 1
        # return list(map(list, ret))

        # More optimal O(n^3) solution which is faster for when numbers repeat in the array nums
        ret = []
        for i in range(n - 3):
            a = nums[i]
            if i > 0 and a == nums[i - 1]:
                continue
            if a + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break
            if a + nums[n - 1] + nums[n - 2] + nums[n - 3] < target:
                continue
            for j in range(i + 1, n - 2):
                b = nums[j]
                if j > i + 1 and b == nums[j - 1]:
                    continue
                if a + b + nums[j + 1] + nums[j + 2] > target:
                    break
                if a + b + nums[n - 1] + nums[n - 2] < target:
                    continue
                rem_target = target - a - b
                start = j + 1
                end = n - 1
                while start < end:
                    c = nums[start]
                    d = nums[end]
                    s = c + d
                    if s == rem_target:
                        ret.append([a, b, c, d])
                        start += 1
                        end -= 1
                        while start < end and nums[start] == nums[start - 1]:
                            start += 1
                        # while end > start and nums[end] == nums[end-1]:
                        #     end -= 1
                    elif s < rem_target:
                        start += 1
                        while start < end - 1 and nums[start] == nums[start - 1]:
                            start += 1
                    else:  # if s > rem_target
                        end -= 1
                        # while end > start + 1 and nums[end] == nums[end-1]:
                        #     end -= 1
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], target: int, expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().fourSum(nums, target)
    if len(set(map(tuple, actual))) != len(actual):
        return False, f"got={actual} has duplicates in it"
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                nums=[1, 0, -1, 0, -2, 2],
                target=0,
                expected=[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]],
            )
            Test(nums=[2, 2, 2, 2, 2], target=8, expected=[[2, 2, 2, 2]])
            Test(
                nums=[
                    1,
                    1,
                    1,
                    1,
                    2,
                    2,
                    2,
                    2,
                    3,
                    3,
                    3,
                    3,
                    4,
                    4,
                    4,
                    4,
                    5,
                    5,
                    5,
                    5,
                    6,
                    6,
                    6,
                    6,
                    7,
                    7,
                    7,
                    7,
                    8,
                    8,
                    8,
                    8,
                ],
                target=18,
                expected=[
                    [1, 1, 8, 8],
                    [1, 2, 7, 8],
                    [1, 3, 6, 8],
                    [1, 3, 7, 7],
                    [1, 4, 5, 8],
                    [1, 4, 6, 7],
                    [1, 5, 5, 7],
                    [1, 5, 6, 6],
                    [2, 2, 6, 8],
                    [2, 2, 7, 7],
                    [2, 3, 5, 8],
                    [2, 3, 6, 7],
                    [2, 4, 4, 8],
                    [2, 4, 5, 7],
                    [2, 4, 6, 6],
                    [2, 5, 5, 6],
                    [3, 3, 4, 8],
                    [3, 3, 5, 7],
                    [3, 3, 6, 6],
                    [3, 4, 4, 7],
                    [3, 4, 5, 6],
                    [3, 5, 5, 5],
                    [4, 4, 4, 6],
                    [4, 4, 5, 5],
                ],
            )
            Test(
                nums=[-1, 0, -5, -2, -2, -4, 0, 1, -2],
                target=-9,
                expected=[
                    [-5, -4, -1, 1],
                    [-5, -4, 0, 0],
                    [-5, -2, -2, 0],
                    [-4, -2, -2, -1],
                ],
            )
            Test(nums=[1], target=0, expected=[])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
