from collections.abc import Callable

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


class MinStack:
    arr: list[tuple[int, int]]  # tuples of (val, min_val_upto_now)

    def __init__(self):
        self.arr = []

    def push(self, value: int) -> None:
        if not self.arr:
            self.arr.append((value, value))
        else:
            self.arr.append((value, min(self.arr[-1][1], value)))

    def pop(self) -> None:
        self.arr.pop()

    def top(self) -> int:
        return self.arr[-1][0]

    def getMin(self) -> int:
        # assuming self.array isn't empty
        return self.arr[-1][1]

    def __str__(self) -> str:
        return str(self.arr)

    def __repr__(self) -> str:
        return self.__str__()


def operate(ops: list[str], values: list[list[int | None]]) -> list[int | None]:
    stack = None

    def per_operate(op: str, val: int | None) -> None | int:
        nonlocal stack
        match op:
            case "MinStack":
                stack = MinStack()
                log(lambda stack=stack: f"stack created => {stack}")
            case "push":
                stack.push(val)
                log(lambda stack=stack: f"pushed {val} into stack => {stack}")
            case "pop":
                stack.pop()
                log(lambda stack=stack: f"stack popped => {stack}")
            case "top":
                val_returned = stack.top()
                log(
                    lambda val_returned=val_returned: (
                        f"Value returned from top = {val_returned}"
                    )
                )
                return val_returned
            case "getMin":
                val_returned = stack.getMin()
                log(
                    lambda val_returned=val_returned: (
                        f"Value returned for getMin = {val_returned}"
                    )
                )
                return val_returned

    ret: list[int | None] = []
    for op, value in zip(ops, values):
        ret.append(per_operate(op, value[0] if value else None))
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    ops: list[str], values: list[int | None], expected: list[int | None]
) -> tuple[bool, str]:
    actual = operate(ops, values)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                ops=[
                    "MinStack",
                    "push",
                    "push",
                    "push",
                    "getMin",
                    "pop",
                    "top",
                    "getMin",
                ],
                values=[[], [-2], [0], [-3], [], [], [], []],
                expected=[None, None, None, None, -3, None, 0, -2],
            )
            # Test( ops =        , values =       , expected =      )
            # Test( ops =        , values =       , expected =      )
            # Test( ops =        , values =       , expected =      )
            # Test( ops =        , values =       , expected =      )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
