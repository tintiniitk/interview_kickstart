class Solution:
    def splitArray(self, nums: list[int]) -> int:
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
                        "Unsupported input with sign changing at > 3 places, not including the nums[0] itself."
                    )
                    return -1
            if cur_diff_sign == 0:
                num_zero_sign_indices += 1
            if num_zero_sign_indices > 1:  # this is excluding [0]
                print(
                    "Unsupported input with #plateaus > 1, not including the nums[0] itself, which can't lead to proper split"
                )
                return -1
            prev_diff_sign = cur_diff_sign
            prev_value = cur_value
        match num_changed_diff_signs:
            case 1:
                if changed_diff_signs[0][1] == 0:
                    print("Improper split")
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
                        print("Improper split")
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
                        print("Improper split")
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
                    print("Improper split")
                    return -1
        return -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().splitArray(nums)
    if actual != expected:
        return False, f"  actual={actual}, expected={expected}"
    return True, ""


def main():
    try:
        with time_limit(5):
            Test(nums=[1, 3, 2], expected=2)
            Test(nums=[1, 2, 4, 3], expected=4)
            Test(nums=[3, 1, 2], expected=-1)
            Test(nums=[64, 36, 2354, 344, 43, 55, 663, 3, 55, 64], expected=-1)
            Test(nums=[1, 3, 5, 5, 4, 2], expected=2)
            Test(nums=[9, 5, 4, 2], expected=2)
            Test(nums=[7, 7, 9], expected=-1)
    except TimeoutException as te:
        print(f"timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
