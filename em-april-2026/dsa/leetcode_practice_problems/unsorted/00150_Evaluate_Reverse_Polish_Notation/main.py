class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []

        def get_operands() -> (int, int):
            val1, val2 = None, None
            if not stack:
                raise ValueError("stack is empty")
            val1 = stack[-1]
            stack.pop()
            if not stack:
                raise ValueError("stack is empty")
            val2 = stack[-1]
            stack.pop()
            return (val1, val2)

        for token in tokens:
            if token == "+":
                o2, o1 = get_operands()
                stack.append(o1 + o2)
            elif token == "-":
                o2, o1 = get_operands()
                stack.append(o1 - o2)
            elif token == "*":
                o2, o1 = get_operands()
                stack.append(o1 * o2)
            elif token == "/":
                o2, o1 = get_operands()
                stack.append(int(o1 / o2))
            else:
                stack.append(int(token))
            # print(f"Stack after handling '{token}' = {stack}")
        if not stack:
            raise ValueError("stack is empty")
        return stack[-1]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(tokens: list[str], expected: int) -> tuple[bool, str]:
    actual = Solution().evalRPN(tokens)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(tokens=["2", "1", "+", "3", "*"], expected=9)
            Test(tokens=["4", "13", "5", "/", "+"], expected=6)
            Test(
                tokens=[
                    "10",
                    "6",
                    "9",
                    "3",
                    "+",
                    "-11",
                    "*",
                    "/",
                    "*",
                    "17",
                    "+",
                    "5",
                    "+",
                ],
                expected=22,
            )
            Test(tokens=["1"], expected=1)
            Test(tokens=["1", "2", "-"], expected=-1)
            Test(tokens=["1", "-2", "/"], expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
