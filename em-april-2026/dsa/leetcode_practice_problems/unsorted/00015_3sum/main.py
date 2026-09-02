class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        if n <= 2:
            return []
        nums.sort()
        print(f"sorted nums = {nums}")
        ret = []
        for i in range(n - 2):
            a = nums[i]
            if i > 0 and a == nums[i - 1]:
                # avoid duplicates
                # print(f"  nums[{start}] == nums[{start-1}] so skipping this")
                continue
            start, end = i + 1, n - 1
            if start >= end:
                continue
            # print(f"for i = {i}, a={a}, start={start}, end={end}")
            if nums[end] + nums[end - 1] < -a:
                # print(f"  nums[{end}] + nums[{end-1}] < -a, so skipping this..")
                continue
            if nums[start] + nums[start + 1] > -a:
                # print(f"  nums[{start}] + nums[{start+1}] > -a, so skipping this..")
                continue
            while end > start:
                b = nums[start]
                c = nums[end]
                # print(f"  trying out b={b}, c={c} at start={start}, end={end}")
                # while start <= end - 2 and b == nums[start+1]:
                #     # print(f"start <= end - 3 and b == nums[start+1] and c == nums[end-1], so start++, end--")
                #     start += 1
                #     # end -= 1
                if b + c == -a:
                    while (
                        start <= end - 3 and b == nums[start + 1] and c == nums[end - 1]
                    ):
                        # print(f"start <= end - 3 and b == nums[start+1] and c == nums[end-1], so start++, end--")
                        start += 1
                        end -= 1
                    ret.append([a, b, c])
                    # print(f"  saving {[a,b,c]} to ret => {ret}")
                    start += 1
                    end -= 1
                elif b + c > -a:
                    end -= 1
                else:
                    start += 1
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().threeSum(nums)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[-1, 0, 1, 2, -1, -4], expected=[[-1, -1, 2], [-1, 0, 1]])
            Test(nums=[0, 1, 1], expected=[])
            Test(nums=[0, 0, 0], expected=[[0, 0, 0]])
            Test(nums=[-1, -1, -1, -1, -1, 0, 1, 1], expected=[[-1, 0, 1]])
            Test(
                nums=[-1, -1, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1],
                expected=[[-1, 0, 1], [0, 0, 0]],
            )
            Test(
                nums=[-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                expected=[[-1, 0, 1], [0, 0, 0]],
            )
            Test(
                nums=[-1, -1, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                expected=[[-1, 0, 1], [0, 0, 0]],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
