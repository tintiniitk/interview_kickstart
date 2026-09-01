SENTINEL_HIGH = 10**4 + 1


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        if n == 1:
            return 0
        last_purchase_price = SENTINEL_HIGH
        quantity_held = 0
        profit = 0
        for i in range(n):
            if quantity_held == 1:
                # try to sell.
                if i == n - 1:
                    if prices[i] > last_purchase_price:
                        # sell
                        profit += prices[i] - last_purchase_price
                        quantity_held = 0
                elif (
                    prices[i] > last_purchase_price
                    and prices[i - 1] <= prices[i] > prices[i + 1]
                ):
                    profit += prices[i] - last_purchase_price
                    quantity_held = 0
            elif quantity_held == 0:
                # try to purchase
                if i == 0:
                    if prices[i] < prices[i + 1]:
                        quantity_held = 1
                        last_purchase_price = prices[i]
                elif i < n - 1 and prices[i - 1] >= prices[i] < prices[i + 1]:
                    quantity_held = 1
                    last_purchase_price = prices[i]
            else:
                raise ValueError(f"quantity_held not in {0, 1}")
        return profit


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
