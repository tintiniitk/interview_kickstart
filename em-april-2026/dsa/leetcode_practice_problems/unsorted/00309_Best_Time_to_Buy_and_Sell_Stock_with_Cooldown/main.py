class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        if n == 1:
            return 0
        max_profit_till_0 = 0
        max_profit_till_1 = max(max_profit_till_0, prices[1] - prices[0])
        if n == 2:
            return max_profit_till_1
        max_profit_ending_on_2 = max(0, prices[2] - prices[1], prices[2] - prices[0])
        max_profit_till_2 = max(max_profit_till_1, max_profit_ending_on_2)
        if n == 3:
            return max_profit_till_2
        (
            max_profit_till_i_minus_3,
            max_profit_till_i_minus_2,
            max_profit_till_i_minus_1,
        ) = max_profit_till_0, max_profit_till_1, max_profit_till_2
        max_profit_ending_on_i_minus_1 = max_profit_ending_on_2
        max_profit_till_i = max_profit_till_2
        for i in range(3, n):
            max_profit_ending_on_i = max(
                0,
                prices[i]
                - prices[i - 1]
                + max(max_profit_till_i_minus_3, max_profit_ending_on_i_minus_1),
            )
            max_profit_till_i = max(max_profit_till_i_minus_1, max_profit_ending_on_i)
            # print(f"at i={i}, max_profit_ending_on_i={max_profit_ending_on_i}, max_profit_till_i={max_profit_till_i}")
            (
                max_profit_till_i_minus_3,
                max_profit_till_i_minus_2,
                max_profit_till_i_minus_1,
            ) = max_profit_till_i_minus_2, max_profit_till_i_minus_1, max_profit_till_i
            max_profit_ending_on_i_minus_1 = max_profit_ending_on_i
        return max_profit_till_i


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(prices: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maxProfit(prices)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(prices=[1, 2, 3, 0, 2], expected=3)
            Test(prices=[1], expected=1)
            Test(prices=[6, 1, 3, 2, 4, 7], expected=6)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
