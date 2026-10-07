def convert_string_sinusoidally(s: str) -> list[str]:
    """
    Args:
     s(str)
    Returns:
     list_str
    """
    # Write your code here.
    n = len(s)
    arrays = [[" " for _ in range(n)] for _ in range(3)]
    for i, c in enumerate(s):
        array_index = 2 if (i % 4 == 0) else 1 if (i % 2 == 1) else 0
        # print(f"i={i}, c={c}, array_index={array_index}")
        arr = arrays[array_index]
        # print(f"  before appending, arr={arr}")
        arr[i] = c
        # print(f"  after appending, arr={arr}")
    return ["".join(arr) for arr in arrays]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: list[str]) -> tuple[bool, str]:
    actual = convert_string_sinusoidally(s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                s="InterviewKickstart",
                expected=[
                    "  t   i   i   t   ",
                    " n e v e K c s a t",
                    "I   r   w   k   r ",
                ],
            )
            Test(s="1aW", expected=["  W", " a ", "1  "])
            Test(s="abc4e", expected=["  c  ", " b 4 ", "a   e"])
            Test(s="1324ab", expected=["  2   ", " 3 4 b", "1   a "])
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
