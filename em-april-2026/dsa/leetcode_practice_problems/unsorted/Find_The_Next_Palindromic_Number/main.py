from math import ceil


def is_palindromic_str(s: str) -> bool:
    return s == s[::-1]


def is_palindromic_num(n: int) -> bool:
    return is_palindromic_str(str(n))


def next_palindrome(n: int) -> int:
    """
    Args:
     n(int32)
    Returns:
     int64
    """

    def next_palindrome_gte(n: int) -> int:
        # base cases for all numbers upto 2 digits
        if n <= 9:
            return n
        if n <= 99:
            return 11 * ceil(n / 11)
        if n <= 101:
            return 101
        if is_palindromic_num(n):
            return n
        n_str = str(n)
        l = len(n_str)
        # l > 2 is guaranteed.
        half = l // 2
        # print(f"for n={n}, l={l}, n_str={n_str}, half={half}, n-half={l - half}")
        first_half_str, middle_digit_str, second_half_str = (
            n_str[:half],
            n_str[half : l - half] if l - half > half else None,
            n_str[l - half :],
        )
        # print(
        #     f"for n={n}, first_half_str, middle_digit_str, second_half_str={(first_half_str, middle_digit_str, second_half_str)}"
        # )
        first_half, middle_digit, second_half = (
            int(first_half_str),
            int(middle_digit_str) if middle_digit_str is not None else None,
            int(second_half_str),
        )
        # print(
        #     f"for n={n}, first_half, middle_digit, second_half={(first_half, middle_digit, second_half)}"
        # )
        rev_of_first_half_str = first_half_str[::-1]
        rev_of_first_half = int(rev_of_first_half_str)
        # obviously, rev_of_first_half != second_half because isn't palindromic.
        if rev_of_first_half > second_half:
            return int(
                "".join(
                    first_half_str
                    + (middle_digit_str if middle_digit_str else "")
                    + rev_of_first_half_str
                )
            )
        if middle_digit and middle_digit < 9:
            return int(
                "".join(first_half_str + str(middle_digit + 1) + rev_of_first_half_str)
            )
        return int(
            "".join(
                str(first_half + 1)
                + ("0" if middle_digit else "")
                + str(first_half + 1)[::-1]
            )
        )

        # rev_of_first_half < second_half
        return n

    return next_palindrome_gte(n + 1)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: int) -> tuple[bool, str]:
    actual = next_palindrome(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=0, expected=1)
            Test(n=10, expected=11)
            Test(n=8, expected=9)
            Test(n=9, expected=11)
            Test(n=10, expected=11)
            Test(n=67, expected=77)
            Test(n=98, expected=99)
            Test(n=99, expected=101)
            Test(n=100, expected=101)
            Test(n=300, expected=303)
            Test(n=1990, expected=1991)
            Test(n=39992, expected=39993)
            Test(n=29993, expected=30003)
            Test(n=29893, expected=29992)
            Test(n=21922, expected=22022)
            Test(n=999, expected=1001)
            Test(n=1000, expected=1001)
            Test(n=1001, expected=1111)
            Test(n=998, expected=999)
            Test(n=997, expected=999)
            Test(n=9999, expected=10001)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
