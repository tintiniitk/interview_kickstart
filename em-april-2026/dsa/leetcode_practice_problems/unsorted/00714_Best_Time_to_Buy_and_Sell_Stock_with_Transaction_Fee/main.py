class Solution:
    def maxProfit(self, prices: list[int], fee: int) -> int:
        if not prices:
            return 0
        n = len(prices)
        if n == 1:
            return 0
        max_profit_till_0: int = 0
        max_profit_ending_on_1: int = prices[1] - prices[0] - fee
        max_profit_till_1: int = max(max_profit_ending_on_1, max_profit_till_0)
        if n == 2:
            return max_profit_till_1
        (
            max_profit_till_i_minus_2,
            max_profit_till_i_minus_1,
        ) = max_profit_till_0, max_profit_till_1
        max_profit_ending_on_i_minus_1: int = max_profit_ending_on_1
        max_profit_till_i: int = 0
        max_profit_till_i_minus_2: int = max_profit_till_0
        max_profit_till_i_minus_1: int = max_profit_till_1
        for i in range(2, n):
            max_profit_ending_on_i = (
                prices[i]
                - prices[i - 1]
                + max(max_profit_till_i_minus_2 - fee, max_profit_ending_on_i_minus_1)
            )
            max_profit_till_i = max(max_profit_till_i_minus_1, max_profit_ending_on_i)
            (
                max_profit_till_i_minus_2,
                max_profit_till_i_minus_1,
            ) = max_profit_till_i_minus_1, max_profit_till_i
            max_profit_ending_on_i_minus_1 = max_profit_ending_on_i
        return max_profit_till_i


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(prices: list[int], fee: int, expected: int) -> tuple[bool, str]:
    actual = Solution().maxProfit(prices, fee)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(prices=[1, 3, 2, 8], fee=2, expected=5)
            Test(prices=[1, 3, 2, 8, 4, 9], fee=2, expected=8)
            Test(prices=[1, 3, 7, 5, 10, 3], fee=3, expected=6)
            Test(prices=[1, 3, 2, 8, 10, 12, 13, 14, 9, 11], fee=2, expected=11)
            Test(prices=[1, 4, 2, 8, 10, 12, 13, 14, 9, 11, 12], fee=2, expected=12)
            Test(
                prices=[1, 2, 1, 3, 1, 4, 2, 8, 10, 12, 13, 14, 9, 11, 12],
                fee=1,
                expected=16,
            )
            Test(
                prices=[1, 1, 3, 2, 1, 2, 1, 3, 2, 2, 3],
                fee=2,
                expected=0,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
