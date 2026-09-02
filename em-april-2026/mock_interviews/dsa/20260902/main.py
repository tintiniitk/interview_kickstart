def max_consecutive_seq_length(nums: list[int]) -> int:
    max_seq = 0
    unique_nums = set(nums)
    max_num = max(unique_nums)
    min_num = min(unique_nums)
    for num in nums:
        if num not in unique_nums:
            continue
        streak = 1
        unique_nums.remove(num)
        k = num + 1
        while k <= max_num and k in unique_nums:
            streak += 1
            unique_nums.remove(k)
            k += 1
        k = num - 1
        while k >= min_num and k in unique_nums:
            streak += 1
            unique_nums.remove(k)
            k -= 1
        max_seq = max(max_seq, streak)
    return max_seq


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = max_consecutive_seq_length(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1], expected=9)
            Test(nums=[5, 3, 2, 9], expected=2)
            Test(nums=[1, 0, 1, 2], expected=3)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
