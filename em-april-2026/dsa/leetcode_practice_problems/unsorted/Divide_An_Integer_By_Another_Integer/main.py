def divide(a: int, b: int) -> int:
    """
    Args:
     a(int64)
     b(int64)
    Returns:
     int64
    """
    # Write your code here.
    # Handle negative numbers if necessary by tracking signs
    sign = -1 if (a < 0) ^ (b < 0) else 1
    a, b = abs(a), abs(b)

    quotient = 0

    # Loop until the remainder is smaller than the divisor
    while a >= b:
        temp_b = b
        multiple = 1

        # Double the divisor and the multiple using addition
        while a >= (temp_b + temp_b):
            temp_b = temp_b + temp_b
            multiple = multiple + multiple

        # Subtract the largest chunk found and add to quotient
        a -= temp_b
        quotient += multiple

    return quotient if sign == 1 else -quotient


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(a: int, b: int, expected: int) -> tuple[bool, str]:
    actual = divide(a, b)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(a=0, b=1, expected=0)
            Test(a=9, b=3, expected=3)
            Test(a=-5, b=2, expected=-2)
            Test(a=-5, b=-2, expected=2)
            Test(a=2147483647, b=1, expected=2147483647)
            Test(a=1, b=2147483647, expected=0)
            Test(a=-2147483647, b=1, expected=-2147483647)
            Test(a=1, b=-2147483648, expected=0)
            Test(a=-30, b=-3, expected=10)
            Test(a=33, b=2, expected=16)
            Test(a=33, b=-2, expected=-16)
            Test(a=5, b=-10, expected=0)
            Test(a=-9000000000000000, b=1, expected=-9000000000000000)
            Test(a=9000000000000000, b=-2, expected=-4500000000000000)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
