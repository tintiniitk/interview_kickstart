from itertools import accumulate


class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        n = len(gas)
        if n != len(cost):
            return -1
        if n == 1:
            return 0 if gas[0] >= cost[0] else -1
        total_gas = sum(gas)
        total_cost = sum(cost)
        if total_gas < total_cost:
            return -1
        extra_gas = [g - c for g, c in zip(gas, cost)]
        # print(f"extra_gas raw = {extra_gas}")
        extra_gas = extra_gas + extra_gas[:-1]  # [0, 1, 2, ... n-1, 0, 1, 2, ... n-2]
        extra_gas = list(accumulate(extra_gas))
        # print(f"extra_gas recycled and accumulated = {extra_gas}")
        m = len(extra_gas)
        started = 0
        streak = 1
        for j in range(1, m):
            if extra_gas[j] >= extra_gas[started]:
                streak += 1
                if streak == n:
                    return (started + 1) % n
            else:
                started = j
                streak = 1
        return -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(gas: list[int], cost: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().canCompleteCircuit(gas, cost)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(gas=[1, 2, 3, 4, 5], cost=[3, 4, 5, 1, 2], expected=3)
            Test(gas=[2, 3, 4], cost=[3, 4, 3], expected=-1)
            Test(gas=[3, 1, 1], cost=[1, 2, 2], expected=0)
            Test(gas=[4], cost=[5], expected=-1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
