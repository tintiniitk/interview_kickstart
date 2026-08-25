class Solution:
    def search(self, nums: list[int], target: int) -> int:
        n = len(nums)
        if n == 1:
            return 0 if nums[0] == target else -1

        # # find index of max-value in [start, end]
        # # it'll return a non-negative value only when found index
        # def find_max_index(start: int, end: int) -> int:
        #     if end < start:
        #         raise ValueError("end < start in find_max_index")
        #         return -1
        #     if end == start:
        #         return start
        #     start_val, end_val = nums[start], nums[end]
        #     if start_val < end_val:
        #         return end
        #     if end - start <= 1:  # only 2 entries remain, the other must be it.
        #         return start
        #     mid = (start + end) // 2
        #     mid_val = nums[mid]
        #     if nums[mid - 1] < mid_val > nums[mid + 1]:
        #         return mid
        #     if start_val < mid_val:
        #         return find_max_index(mid, end)
        #     else:
        #         return find_max_index(start, mid)

        # max_index = find_max_index(0, n - 1)
        # min_index = (
        #     max_index + 1
        # ) % n  # treating the array as circular i.e. nums[n+k] = nums[k]
        # # print(f"max_index = {max_index}, min_index = {min_index}")

        # # find index of target in [start, end], with 0 <= min_index <= start <= end <= max_index <= 2*n-1
        # # it'll return a non-negative value only when found index
        # def find_target_index(start: int, end: int) -> int:
        #     if end < start:
        #         raise ValueError("end < start in find_target_index")
        #         return -1
        #     start_val = nums[start % n]
        #     if start_val == target:
        #         return start
        #     if start_val > target:
        #         return -1
        #     if end == start:
        #         return -1
        #     end_val = nums[end % n]
        #     if end_val < target:
        #         return -1
        #     if end - start <= 1:  # only 2 entries remain, the other must be it.
        #         if end_val == target:
        #             return end
        #         return -1
        #     mid = (start + end) // 2
        #     mid_val = nums[mid % n]
        #     if mid_val == target:
        #         return mid
        #     if target < mid_val:
        #         return find_target_index(start, mid - 1)
        #     else:
        #         return find_target_index(mid + 1, end)

        # found_index = find_target_index(
        #     min_index, max_index if max_index == n - 1 else n + max_index
        # )
        # return found_index % n if found_index >= 0 else -1

        l, r = 0, n - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            if nums[m] < nums[r]:
                # right half is sorted
                if nums[m] < target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1
            else:
                # left half is sorted
                if nums[m] > target >= nums[l]:
                    r = m - 1
                else:
                    l = m + 1
        return -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], target: int, expected: int) -> tuple[bool, str]:
    actual = Solution().search(nums, target)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[2, 5, 6, 0, 1, 2], target=0, expected=3)
            Test(nums=[2, 5, 6, 0, 1, 2], target=3, expected=-1)
            Test(nums=[4, 5, 6, 7, 0, 1, 2], target=0, expected=4)
            Test(nums=[4, 5, 6, 7, 0, 1, 2], target=3, expected=-1)
            Test(nums=[1], target=0, expected=-1)
            Test(nums=[1, 3], target=1, expected=0)
            Test(
                nums=[
                    6,
                    8,
                    10,
                    13,
                    16,
                    17,
                    20,
                    21,
                    22,
                    23,
                    25,
                    27,
                    29,
                    34,
                    37,
                    38,
                    42,
                    44,
                    45,
                    50,
                    51,
                    52,
                    53,
                    55,
                    60,
                    62,
                    63,
                    64,
                    65,
                    68,
                    70,
                    75,
                    79,
                    80,
                    84,
                    88,
                    94,
                ],
                target=37,
                expected=14,
            )
            Test(
                nums=[
                    6,
                    8,
                    10,
                    13,
                    16,
                    17,
                    20,
                    21,
                    22,
                    23,
                    25,
                    27,
                    29,
                    34,
                    37,
                    38,
                    42,
                    44,
                    45,
                    50,
                    51,
                    52,
                    53,
                    55,
                    60,
                    62,
                    63,
                    64,
                    65,
                    68,
                    70,
                    75,
                    79,
                    80,
                    84,
                    88,
                    94,
                ],
                target=36,
                expected=-1,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
