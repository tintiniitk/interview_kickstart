MOD = 7 + 10**9


def get_product_array(nums: list[int]) -> list[int]:
    """
    Args:
     nums(list_int32)
    Returns:
     list_int32
    """
    # Write your code here.
    n = len(nums)
    ret = [1] * n
    # print(f"n={n}, nums={nums}, ret={ret}")
    for i in range(1, n):
        ret[i] = (ret[i - 1] * nums[i - 1]) % MOD
    # print(f"intermediate ret={ret}")
    right = 1
    for i in range(n - 2, -1, -1):
        right = (right * nums[i + 1]) % MOD
        ret[i] = (ret[i] * right) % MOD
    # print(f"final ret={ret}")
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = get_product_array(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 2, 3, 4, 5], expected=[120, 60, 40, 30, 24])
            Test(nums=[0, 1000000000], expected=[1000000000, 0])
            Test(nums=[-1000000000, 0], expected=[0, 7])
            Test(
                nums=[84107501, 258139847, -123134593],
                expected=[225074344, 168613708, 287711868],
            )
            Test(nums=[10, 0, -10], expected=[0, 999999907, 0])
            Test(
                nums=[
                    1408134,
                    -4813041,
                    34314135,
                    -23523,
                    67857984,
                    35624578,
                    56378345,
                    638456,
                    -152464,
                    5246,
                ],
                expected=[
                    330556655,
                    229416069,
                    706466103,
                    684859012,
                    861964518,
                    258822887,
                    276694326,
                    663773329,
                    519846908,
                    403747920,
                ],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
