def sum_zero(arr: list[int]) -> list[int]:
    """
    Args:
     arr(list_int32)
    Returns:
     list_int32
    """
    # Write your code here.
    prefix_sums_mappings = {0: -1}
    prefix_sum = 0
    for i, num in enumerate(arr):
        prefix_sum += num
        if prefix_sum in prefix_sums_mappings:
            return [prefix_sums_mappings[prefix_sum] + 1, i]
        prefix_sums_mappings[prefix_sum] = i
    return [-1]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(arr: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = sum_zero(arr)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(arr=[5, 1, 2, -3, 7, -4], expected=[1, 3])
            Test(arr=[1, 2, 3, 5, -9], expected=[-1])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
