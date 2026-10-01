def find_max_length_of_matching_parentheses(brackets: str):
    """
    Args:
     brackets(str)
    Returns:
     int32
    """
    s: list[int | str] = []
    for b in brackets:
        if not s:
            s.append(b)
            # last_bracket_was_open = b == '('
        elif b == ")":
            if s[-1] == "(":
                s.pop()  # remove preceding opening bracket.
                count = 2
                # if there was a number before this number, then fuse these two numbers into one.
                if s and s[-1] not in {"(", ")"} and isinstance(s[-1], int):
                    count += int(s[-1])
                    s.pop()
                s.append(count)
            elif s[-1] != ")":
                # previous entry in s was a number.
                # if before the number was an opening bracket, then this can be combined.
                if len(s) > 1 and s[-2] == "(":
                    count = s[-1]
                    assert isinstance(count, int)
                    s.pop()  # remove the number
                    s.pop()  # remove the opening bracket
                    # if there was a number before this number, then fuse these two numbers into one.
                    if s and s[-1] not in {"(", ")"} and isinstance(s[-1], int):
                        count += int(s[-1])
                        s.pop()
                    s.append(count + 2)  # insert the new count in its place.
                else:
                    s.append(b)
            else:
                s.append(b)
        else:
            s.append(b)
    # print(f"after parsing, s='{s}'")
    only_ints_from_s = [entry for entry in s if isinstance(entry, int)]
    return max(only_ints_from_s) if only_ints_from_s else 0


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(brackets: str, expected: int) -> tuple[bool, str]:
    actual = find_max_length_of_matching_parentheses(brackets)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(brackets="((((())(((()", expected=4)
            Test(brackets="()()()", expected=6)
            Test(brackets="(", expected=0)
            Test(brackets=")", expected=0)
            Test(brackets="()", expected=2)
            Test(brackets="((", expected=0)
            Test(brackets="()((()))()((()))", expected=16)
            Test(brackets="))(())((", expected=4)
            Test(brackets="((((())))()(())(())()())())", expected=26)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
