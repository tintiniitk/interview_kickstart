from heapq import heappop, heappush


class MedianFinder:
    low_pq: list[int]  # max-heap containing the negatives of the lowest n+1//2 numbers
    high_pq: list[int]  # min-heap containing the the highest n//2 numbers
    n1: int
    n2: int

    def __init__(self):
        self.low_pq = []
        self.high_pq = []
        self.n1 = self.n2 = 0

    def addNum(self, num: int) -> None:
        n1, n2 = self.n1, self.n2
        if n1 == n2 == 0:
            # push num to to self.low_pq
            heappush(self.low_pq, -num)
            self.n1 += 1
        else:
            low_max = -self.low_pq[0]
            if num < low_max:
                # it must go to low_pq
                if self.n1 > self.n2:
                    # pop one from self.low_pq
                    heappop(self.low_pq)
                    # and push it to self.high_pq
                    heappush(self.high_pq, low_max)
                    self.n1 -= 1
                    self.n2 += 1
                # push negative of num to to self.low_pq
                heappush(self.low_pq, -num)
                self.n1 += 1
            else:
                if self.n2 == 0 or num > self.high_pq[0]:
                    # it must go to high_pq
                    if self.n1 == self.n2:
                        high_min = self.high_pq[0]
                        # pop one from self.high_pq
                        heappop(self.high_pq)
                        # and push it to self.low_pq
                        heappush(self.low_pq, -high_min)
                        self.n2 -= 1
                        self.n1 += 1
                    # push num to to self.high_pq
                    heappush(self.high_pq, num)
                    # update count of self.low_pq
                    self.n2 += 1
                else:
                    # it could go to either to keep the balance.
                    if self.n2 >= self.n1:
                        # its negative should go to self.low_pq
                        heappush(self.low_pq, -num)
                        # update count of self.low_pq
                        self.n1 += 1
                    else:
                        # it should go to self.high_pq
                        heappush(self.high_pq, num)
                        # update count of self.high_pq
                        self.n2 += 1

    def findMedian(self) -> float:
        if self.n1 > self.n2:
            return -self.low_pq[0]
        else:
            return (-self.low_pq[0] + self.high_pq[0]) / 2


def operate(ops: list[str], values: list[list[int]]) -> list[float | None]:
    medianFinder: MedianFinder | None = None
    ret = []
    for op, value in zip(ops, values):
        match op:
            case "MedianFinder":
                medianFinder = MedianFinder()
                ret.append(None)
            case "addNum":
                assert medianFinder and isinstance(medianFinder, MedianFinder)
                assert value
                num = value[0]
                medianFinder.addNum(num)
                ret.append(None)
            case "findMedian":
                assert medianFinder and isinstance(medianFinder, MedianFinder)
                ret.append(medianFinder.findMedian())
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    ops: list[str], values: list[list[int]], expected: list[float | None]
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
                    "MedianFinder",
                    "addNum",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                ],
                values=[[], [1], [2], [], [3], []],
                expected=[None, None, None, 1.50000, None, 2.00000],
            )
            Test(
                ops=[
                    "MedianFinder",
                    "addNum",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                ],
                values=[[], [2], [1], [], [3], []],
                expected=[None, None, None, 1.50000, None, 2.00000],
            )
            Test(
                ops=[
                    "MedianFinder",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                    "addNum",
                    "findMedian",
                ],
                values=[[], [1], [], [3], [], [-1], [], [4], [], [1], [], [1], []],
                expected=[
                    None,
                    None,
                    1.00000,
                    None,
                    2.00000,
                    None,
                    1.00000,
                    None,
                    2.00000,
                    None,
                    1.00000,
                    None,
                    1.00000,
                ],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
