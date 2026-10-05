SENTINEL_HIGH = 10**4 + 1


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if not prices:
            return 0
        n = len(prices)
        if n == 1:
            return 0

        # # my original solution
        # prev_price = prices[0]
        # buy_price = prev_price if prev_price <= prices[1] else SENTINEL_HIGH
        # # if buy_price < SENTINEL_HIGH:
        # # print(f"buy on day#0 for {buy_price}")
        # total_profit = 0
        # for i in range(1, n - 1):
        #     price = prices[i]
        #     if prev_price <= price > prices[i + 1]:
        #         profit = max(price - buy_price, 0)
        #         total_profit += profit
        #         # print(f"sold on day#{i} for profit={profit}, total_profit={total_profit}")
        #         buy_price = SENTINEL_HIGH
        #     if buy_price > price and prev_price >= price < prices[i + 1]:
        #         buy_price = price
        #         # print(f"buy on day#{i} for {buy_price}")
        #     prev_price = price
        # profit = max(prices[n - 1] - buy_price, 0)
        # total_profit += profit
        # # print(f"sold on day#{n-1} for profit={profit}, total_profit={total_profit}")
        # return total_profit

        # alternate solution suggested by IK
        max_profit_till_0 = 0
        max_profit_ending_on_1 = max(0, prices[1] - prices[0])
        max_profit_till_1 = max_profit_ending_on_1
        if n == 2:
            return max_profit_till_1
        (
            max_profit_till_i_minus_2,
            max_profit_till_i_minus_1,
        ) = max_profit_till_0, max_profit_till_1
        max_profit_ending_on_i_minus_1 = max_profit_ending_on_1
        max_profit_till_i = max_profit_till_1
        for i in range(2, n):
            max_profit_ending_on_i = max(
                0,
                prices[i]
                - prices[i - 1]
                + max(max_profit_till_i_minus_2, max_profit_ending_on_i_minus_1),
            )
            max_profit_till_i = max(max_profit_till_i_minus_1, max_profit_ending_on_i)
            # print(f"at i={i}, max_profit_ending_on_i={max_profit_ending_on_i}, max_profit_till_i={max_profit_till_i}")
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
def Test(prices: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maxProfit(prices)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(prices=[7, 1, 5, 3, 6, 4], expected=7)
            Test(prices=[1, 2, 3, 4, 5], expected=4)
            Test(prices=[7, 6, 4, 3, 1], expected=0)
            Test(prices=[], expected=0)
            Test(prices=[1], expected=0)
            Test(prices=[1, 2, 3, 2, 1, 1, 1, 4, 5, 6, 6, 4], expected=7)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
