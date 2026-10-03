MOD = 7 + 10**9

from itertools import pairwise


def find_pascal_triangle(n: int) -> list[list[int]]:
    """
    Args:
     n(int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    ret = [[1]]
    for i in range(1, n):
        prev_row = ret[-1]
        row = [1] + [(num1 + num2) % MOD for num1, num2 in pairwise(prev_row)] + [1]
        ret.append(row)
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.1, stop_on_tc_failure=False)
def Test(n: int, expected: list[list[int]]) -> tuple[bool, str]:
    actual = find_pascal_triangle(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=4, expected=[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]])
            Test(n=5, expected=[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]])
            Test(
                n=6,
                expected=[
                    [1],
                    [1, 1],
                    [1, 2, 1],
                    [1, 3, 3, 1],
                    [1, 4, 6, 4, 1],
                    [1, 5, 10, 10, 5, 1],
                ],
            )
            Test(
                n=7,
                expected=[
                    [1],
                    [1, 1],
                    [1, 2, 1],
                    [1, 3, 3, 1],
                    [1, 4, 6, 4, 1],
                    [1, 5, 10, 10, 5, 1],
                    [1, 6, 15, 20, 15, 6, 1],
                ],
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
