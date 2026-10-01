class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        capacity_utilized_at_time = [0] * 1001
        for num_passengers, start, end in trips:
            if num_passengers > capacity:
                return False
            capacity_utilized_at_time[start] += num_passengers
            capacity_utilized_at_time[end] -= num_passengers
        existing_capacity = capacity
        for capacity_utilized_at_t in capacity_utilized_at_time:
            if capacity_utilized_at_t != 0:
                existing_capacity -= capacity_utilized_at_t
                if existing_capacity < 0:
                    return False
        return True


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(trips: list[list[int]], capacity: int, expected: int) -> tuple[bool, str]:
    actual = Solution().carPooling(trips, capacity)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(trips=[[2, 1, 5], [3, 3, 7]], capacity=4, expected=False)
            Test(trips=[[2, 1, 5], [3, 3, 7]], capacity=5, expected=True)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
