from typing import List
from itertools import pairwise


class Solution:
    def splitArray(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            raise ValueError(f"Improper input length: {n}, expected at least: 2")
        if n == 2:
            return abs(nums[0] - nums[1])
        changed_diff_signs = []  # index->sign
        prev_diff_sign = 0  # initial at [0]
        prev_value = nums[0]
        num_zero_sign_indices = 0
        num_changed_diff_signs = 0
        for i in range(1, n):
            cur_value = nums[i]
            cur_diff_sign = (
                1 if cur_value > prev_value else (-1 if cur_value < prev_value else 0)
            )
            if cur_diff_sign == 0 or cur_diff_sign != prev_diff_sign:
                changed_diff_signs.append((i, cur_diff_sign))
                num_changed_diff_signs += 1
                if num_changed_diff_signs > 3:  # this is excluding [0]
                    print(
                        f"Unsupported input with sign changing at > 3 places, not including the nums[0] itself."
                    )
                    return -1
            if cur_diff_sign == 0:
                num_zero_sign_indices += 1
            if num_zero_sign_indices > 1:  # this is excluding [0]
                print(
                    f"Unsupported input with #plateaus > 1, not including the nums[0] itself, which can't lead to proper split"
                )
                return -1
            prev_diff_sign = cur_diff_sign
            prev_value = cur_value
        match num_changed_diff_signs:
            case 1:
                if changed_diff_signs[0][1] == 0:
                    print(f"Improper split")
                    return -1
                elif changed_diff_signs[0][1] > 0:
                    # nums is strictly increasing throughout.
                    sum_nums = sum(nums)
                    return abs(sum_nums - 2 * nums[-1])
                else:
                    # nums is strictly decreasing throughout.
                    sum_nums = sum(nums)
                    return abs(sum_nums - 2 * nums[0])
            case 2:
                if num_zero_sign_indices == 0:
                    if not (
                        changed_diff_signs[0][1] > 0 and changed_diff_signs[1][1] < 0
                    ):
                        print(f"Improper split")
                        return -1
                    second_sign_change_index = changed_diff_signs[1][0]
                    return min(
                        (
                            abs(
                                sum(nums[:second_sign_change_index])
                                - sum(nums[second_sign_change_index:])
                            )
                        ),
                        (
                            abs(
                                sum(nums[: second_sign_change_index - 1])
                                - sum(nums[second_sign_change_index - 1 :])
                            )
                        ),
                    )
                else:  # num_zero_sign_indices == 1
                    if changed_diff_signs[0][1] == 0 and changed_diff_signs[1][1] < 0:
                        return abs(sum(nums) - 2 * nums[0])
                    elif changed_diff_signs[0][1] > 0 and changed_diff_signs[1][1] == 0:
                        return abs(sum(nums) - 2 * nums[-1])
                    else:
                        print(f"Improper split")
                        return -1
            case 3:
                if (
                    changed_diff_signs[0][1] > 0
                    and changed_diff_signs[1][1] == 0
                    and changed_diff_signs[2][1] < 0
                ):
                    plateau_start_index = changed_diff_signs[1][0] - 1
                    plateau_end = plateau_start_index + 1
                    return abs(sum(nums[:plateau_end]) - sum(nums[plateau_end:]))
                else:
                    print(f"Improper split")
                    return -1
        return -1


def Test(nums: List[int], expected: int):
    print(f"#### Test case: nums={nums}, expected={expected} ...")
    actual = Solution().splitArray(nums)
    assert (
        actual == expected
    ), f"  ! Failed actual={actual}, expected={expected} for nums={nums}"
    print(f"  ! Passed !")


Test([1, 3, 2], 2)
Test([1, 2, 4, 3], 4)
Test([3, 1, 2], -1)
Test([64, 36, 2354, 344, 43, 55, 663, 3, 55, 64], -1)
Test([1, 3, 5, 5, 4, 2], 2)
Test([9, 5, 4, 2], 2)
Test([7, 7, 9], -1)
