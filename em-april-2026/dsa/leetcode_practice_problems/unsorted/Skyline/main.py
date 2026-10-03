from collections import defaultdict
from heapq import heappop, heappush


class MySortedList:
    pq: list[int]
    freq: dict[int, int]

    def __init__(self):
        self.pq: list[int] = []
        self.freq: dict[int, int] = defaultdict(int)

    def add(self, v: int):
        # print(f"add({v})")
        heappush(self.pq, -v)
        self.freq[-v] += 1
        # print(f"add({v}) => pq={self.pq}, freq={dict(self.freq)}")

    def remove(self, v: int):
        # print(f"remove({v})")
        assert -v in self.freq and self.freq[-v] > 0
        if self.pq[0] == -v:
            heappop(self.pq)
        if self.freq[-v] == 1:
            del self.freq[-v]
        else:
            self.freq[-v] -= 1
        # print(f"remove({v}) => pq={self.pq}, freq={dict(self.freq)}")

    def max(self) -> int:
        # print("max() => ")
        neg_top = self.pq[0]
        while True:
            if neg_top not in self.freq or self.freq[neg_top] <= 0:
                # print(
                #     f"  found invalid entry {neg_top} on top, with freq={dict(self.freq)}"
                # )
                heappop(self.pq)
            else:
                # print(f"  found entry {neg_top} on top")
                break
            neg_top = self.pq[0]
        # print(f"max() => {-neg_top}")
        return -neg_top

    def __bool__(self) -> bool:
        ret = bool(
            self is not None
            and self.pq is not None
            and self.pq
            and self.freq is not None
            and self.freq
        )
        # if not ret:
        #     print(f"__bool__() => {ret}")
        return ret


def find_skyline(buildings: list[list[int]]) -> list[list[int]]:
    """
    Args:
     buildings(list_list_int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    start_end_points = []
    for start, end, h in buildings:
        if h == 0:
            continue
        start_end_points.append((start, -h))
        start_end_points.append((end, h))
    start_end_points.sort()
    # print(f"start_end_points={start_end_points}")

    segments = []
    sorted_heights_active = MySortedList()
    current_max_height = 0
    for x, h in start_end_points:
        if h < 0:
            sorted_heights_active.add(-h)
        else:  # h > 0
            sorted_heights_active.remove(h)

        if sorted_heights_active:
            max_active_height = sorted_heights_active.max()
            if max_active_height != current_max_height:
                current_max_height = max_active_height
                segments.append([x, current_max_height])
        elif current_max_height != 0:
            current_max_height = 0
            segments.append([x, current_max_height])

    return segments


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(buildings: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    actual = find_skyline(buildings)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                buildings=[
                    [2, 9, 10],
                    [3, 7, 15],
                    [5, 12, 12],
                    [15, 20, 10],
                    [19, 24, 8],
                ],
                expected=[
                    [2, 10],
                    [3, 15],
                    [7, 12],
                    [12, 0],
                    [15, 10],
                    [20, 8],
                    [24, 0],
                ],
            )
            # Test(buildings=    , expected=  )
            # Test(buildings=    , expected=  )
            # Test(buildings=    , expected=  )
            # Test(buildings=    , expected=  )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
