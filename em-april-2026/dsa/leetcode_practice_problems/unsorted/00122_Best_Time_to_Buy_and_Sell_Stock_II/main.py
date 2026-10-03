SENTINEL_HIGH = 10**4 + 1


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if not prices:
            return 0
        n = len(prices)
        if n == 1:
            return 0

        prev_price = prices[0]
        buy_price = prev_price if prev_price <= prices[1] else SENTINEL_HIGH
        # if buy_price < SENTINEL_HIGH:
        # print(f"buy on day#0 for {buy_price}")
        total_profit = 0
        for i in range(1, n - 1):
            price = prices[i]
            if prev_price <= price > prices[i + 1]:
                profit = max(price - buy_price, 0)
                total_profit += profit
                # print(f"sold on day#{i} for profit={profit}, total_profit={total_profit}")
                buy_price = SENTINEL_HIGH
            if buy_price > price and prev_price >= price < prices[i + 1]:
                buy_price = price
                # print(f"buy on day#{i} for {buy_price}")
            prev_price = price
        profit = max(prices[n - 1] - buy_price, 0)
        total_profit += profit
        # print(f"sold on day#{n-1} for profit={profit}, total_profit={total_profit}")
        return total_profit


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
