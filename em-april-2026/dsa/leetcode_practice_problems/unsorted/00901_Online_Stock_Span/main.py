class StockSpanner:
    i: int = 0
    stack: list[
        tuple[int, int, int]
    ]  # list of (index, stock-value, span-value) wherever stock value fell in the next entry
    prev_stock_price: int = -1
    prev_span: int = 0

    def __init__(self):
        self.stack: list[tuple[int, int, int]] = []
        self.prev_stock_price: int = -1
        self.prev_span: int = 0

    def next(self, price: int) -> int:
        span = 1
        if self.i > 0:
            if price >= self.prev_stock_price:
                if self.stack:
                    while self.stack:
                        if price >= self.stack[-1][1]:
                            span = self.stack[-1][2] + self.i - self.stack[-1][0]
                            self.stack.pop()
                        else:
                            span = self.i - self.stack[-1][0]
                            break
                else:
                    span = 1 + self.prev_span
            else:
                self.stack.append((self.i - 1, self.prev_stock_price, self.prev_span))
        self.prev_stock_price = price
        self.prev_span = span
        self.i += 1
        return span


def operate(operations: list[str], values: list[list[int]]) -> list[int | None]:
    ret = []
    ss = None
    for i, operation in enumerate(operations):
        match operation:
            case "StockSpanner":
                ss = StockSpanner()
                ret.append(None)
            case "next":
                if not ss:
                    raise ValueError("next called before StockSpanner!")
                ret.append(ss.next(values[i][0]))
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    operations: list[str], values: list[list[int]], expected: list[int | None]
) -> tuple[bool, str]:
    actual = operate(operations, values)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                operations=[
                    "StockSpanner",
                    "next",
                    "next",
                    "next",
                    "next",
                    "next",
                    "next",
                    "next",
                ],
                values=[[], [100], [80], [60], [70], [60], [75], [85]],
                expected=[None, 1, 1, 1, 2, 1, 4, 6],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
