import string
from collections.abc import Callable
from typing import Any

from utils.pretty_test_runner import truncate_param

DEBUGGING = False


def log(log_factory: Callable[[], object], force_enabled: bool = False) -> None:
    if DEBUGGING or force_enabled:
        print(log_factory())


class FailedToParseException(Exception):
    def __init__(self, expression: list[Any] | str, message: str = "Unknown reason"):
        truncated_expr_str = (
            truncate_param("".join(map(str, expression)), max_str=100)
            if isinstance(expression, (list, set, tuple))
            else truncate_param(expression, max_str=100)
        )
        super().__init__(f"Expression: {truncated_expr_str}. Reason: {message}")


def is_valid(expression: str) -> bool:
    """
    Args:
     expression(str)
    Returns:
     bool
    """
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
    }
    digits = set(string.digits)
    opening_brackets = ["(", "{", "["]
    closing_brackets = [")", "]", "}"]
    brackets = opening_brackets + closing_brackets
    matching_open_bracket = {")": "(", "]": "[", "}": "{"}
    brackets_and_ops = set(brackets + list(ops.keys()))

    # combine all consecutive digits into single digits e.g. [..., '2', '1', '3', ...] => [..., 213, ...]
    def collasce_digits(s: list[str | int]) -> list[str | int]:
        s2 = []
        for c in s:
            if c in digits:
                if s2 and isinstance(s2[-1], int):
                    s2[-1] = s2[-1] * 10 + int(c)
                else:
                    s2.append(int(c))
            else:
                s2.append(c)
        return s2

    # combine all plain number operations without any brackets involved e.g. [..., 10, '+', '2', ... ] => [..., 12, ...]
    def reduce_simple_operations(s: list[str | int]) -> list[str | int]:
        s2 = []
        for token in s:
            if isinstance(token, int):
                while len(s2) >= 2:
                    prev_token = s2[-1]
                    prev_to_prev_token = s2[-2]
                    if prev_token in ops and isinstance(prev_to_prev_token, int):
                        s2.pop()
                        s2.pop()
                        token = ops[prev_token](prev_to_prev_token, token)
                    else:
                        break
            s2.append(token)
        return s2

    # combine all plain brackets without any operations involved e.g. [..., '(', 2, ')', ... ] => [..., 2, ...], or  [..., '[', ']', ... ] => [..., ...]
    # or flagging bad input e.g. [..., '(', ']', ... ] => Error!
    def reduce_simple_brackets(s: list[str | int]) -> list[str | int]:
        s2 = []
        for token in s:
            if token in closing_brackets:
                if s2:
                    prev_token = s2[-1]
                    if prev_token == matching_open_bracket[token]:
                        s2.pop()
                        continue
                    if prev_token in closing_brackets:
                        s2.append(token)
                        continue
                    elif prev_token in opening_brackets:
                        raise FailedToParseException(
                            expression=s,
                            message=f"closing bracket {token} preceded by a non-matching opening bracket '{prev_token}'",
                        )
                    elif not isinstance(prev_token, int):
                        raise FailedToParseException(
                            expression=s,
                            message=f"closing bracket {token} preceded by an unexpected token '{prev_token}'",
                        )
                    elif len(s2) >= 2:
                        prev_to_prev_token = s2[-2]
                        if prev_to_prev_token == matching_open_bracket[token]:
                            s2.pop()
                            s2.pop()
                            s2.append(prev_token)
                            continue
                        elif prev_to_prev_token in opening_brackets:
                            raise FailedToParseException(
                                expression=s,
                                message=f"closing bracket {token} preceded by number {prev_token} preceded by a non-matching opening bracket '{prev_to_prev_token}'",
                            )
                        elif prev_to_prev_token not in ops:
                            raise FailedToParseException(
                                s,
                                message=f"closing bracket {token} preceded by number {prev_token} preceded by an unexpected token '{prev_to_prev_token}'",
                            )
                else:
                    raise FailedToParseException(
                        s,
                        message=f"the expression is starting with a closing bracket {token}",
                    )
            elif token in opening_brackets:
                pass
            s2.append(token)
        return s2

    input: list[str | int] = list(expression)
    num_passes = 0
    try:
        # initial cleanup
        output = collasce_digits(input)
        num_passes += 1
        log(
            lambda: (
                f"after pass#{num_passes}: {truncate_param(''.join(map(str, output)), max_str=100)}"
            )
        )
        if not output or (len(output) == 1 and isinstance(output[0], int)):
            return True
        if len(output) == 1 and not isinstance(output[0], int):
            raise FailedToParseException(
                expression="".join(map(str, input)),
                message=f"reduced expression {''.join(map(str, output))} is invalid",
            )
        while output and (
            len(output) > 1 or any(token in brackets_and_ops for token in output)
        ):
            input = output
            output1 = reduce_simple_operations(input)
            num_passes += 1
            log(
                lambda num_passes=num_passes, output1=output1: (
                    f"after pass#{num_passes}: {truncate_param(''.join(map(str, output1)), max_str=100)}"
                )
            )
            if not output1 or (len(output1) == 1 and isinstance(output1[0], int)):
                return True
            if len(output1) == 1 and not isinstance(output1[0], int):
                raise FailedToParseException(
                    expression="".join(map(str, input)),
                    message=f"reduced expression {''.join(map(str, output1))} is invalid",
                )
            output = reduce_simple_brackets(output1)
            num_passes += 1
            log(
                lambda num_passes=num_passes, output=output: (
                    f"after pass#{num_passes}: {truncate_param(''.join(map(str, output)), max_str=100)}"
                )
            )
            if not output or (len(output) == 1 and isinstance(output[0], int)):
                return True
            if len(output) == 1 and not isinstance(output[0], int):
                raise FailedToParseException(
                    expression="".join(map(str, input)),
                    message=f"reduced expression {''.join(map(str, output))} is invalid",
                )
            if len(output) == len(input):
                raise FailedToParseException(
                    expression="".join(map(str, input)),
                    message="last two passes didn't reduce the expression at all",
                )
        return False
    except FailedToParseException as fe:
        log(lambda fe=fe: f"{fe}", force_enabled=True)
        return False

    return True


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=False)
def Test(expression: str, expected: bool) -> tuple[bool, str]:
    actual = is_valid(expression)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(expression="{(12+21)*35}+45", expected=True)
            Test(expression="{(1+2)*3}+4", expected=True)
            Test(expression="((1+2)*3*)", expected=False)
            Test(expression="()()[]{}", expected=True)
            Test(expression="(", expected=False)
            Test(expression="((", expected=False)
            Test(expression="1+(", expected=False)
            Test(expression="{2+1+(3+4)}", expected=True)
            Test(expression="}", expected=False)
            Test(expression="{[()]}", expected=True)
            Test(expression="(1+2]", expected=False)
            Test(expression="[{2*1}+(10-5-[1-2])]", expected=True)
            Test(expression="{[(1*2*3*4)+(5+6+7+8)]}", expected=True)
            Test(expression="{{[(1*2*3*4)+(5+6+7+8)]}", expected=False)
            Test(expression="{5}{5}", expected=False)
            Test(expression="{5+[{4/10}-(10-5)]}", expected=True)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
