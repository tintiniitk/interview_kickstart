"""
# old outdated complex approach,
# which ran into issues and hence abandoned.

type Streak = tuple[int, int]
type Streaks = list[Streak]
type StreakIndexSpan = tuple[int, int]


def find_streaks_of_increasing_prices(prices: list[int]) -> Streaks:
    n = len(prices)
    if len(prices) < 2:
        return []
    streak_start_index = 0 if prices[0] < prices[1] else -1
    streaks = []
    for i in range(1, n):
        if prices[i - 1] < prices[i]:
            if streak_start_index != -1 and (i == n - 1 or prices[i] >= prices[i + 1]):
                streaks.append((streak_start_index, i))
                streak_start_index = -1
        elif i < n - 1 and prices[i + 1] > prices[i] and streak_start_index == -1:
            streak_start_index = i
    return streaks


def find_max_profit_upto_ith_streak_from_first_streak(
    prices: list[int],
    streaks: Streaks,
) -> tuple[list[StreakIndexSpan], list[int]]:
    num_streaks = len(streaks)
    first_streak_profit = prices[streaks[0][1]] - prices[streaks[0][0]]
    if num_streaks == 1:
        return ([(0, 0)], [first_streak_profit])
    max_profit_streak_pairs_upto_streak_i = [(0, 0)]
    max_streak_profit_upto_i = [first_streak_profit]
    for i in range(1, num_streaks):
        max_profit_upto_ith_streak_pair = max_profit_streak_pairs_upto_streak_i[i - 1]
        max_profit_upto_ith_streak = max_streak_profit_upto_i[i - 1]
        if (
            prices[streaks[i][1]]
            > prices[streaks[max_profit_upto_ith_streak_pair[1]][1]]
        ):
            max_profit_upto_ith_streak = (
                prices[streaks[i][1]]
                - prices[streaks[max_profit_upto_ith_streak_pair[0]][0]]
            )
            max_profit_upto_ith_streak_pair = (
                max_profit_upto_ith_streak_pair[0],
                i,
            )
        if prices[streaks[i][1]] - prices[streaks[i][0]] > max_profit_upto_ith_streak:
            max_profit_upto_ith_streak_pair = (i, i)
            max_profit_upto_ith_streak = prices[streaks[i][1]] - prices[streaks[i][0]]
        max_profit_streak_pairs_upto_streak_i.append(max_profit_upto_ith_streak_pair)
        max_streak_profit_upto_i.append(max_profit_upto_ith_streak)
    return max_profit_streak_pairs_upto_streak_i, max_streak_profit_upto_i


def find_max_streak_profit_upto_ith_streak_from_last_streak(
    prices: list[int],
    streaks: Streaks,
) -> tuple[list[StreakIndexSpan], list[int]]:
    num_streaks = len(streaks)
    last_streak_profit = (
        prices[streaks[num_streaks - 1][1]] - prices[streaks[num_streaks - 1][0]]
    )
    if num_streaks == 1:
        return ([(num_streaks - 1, num_streaks - 1)], [last_streak_profit])
    max_profit_streak_pairs_upto_streak_i = [(num_streaks - 1, num_streaks - 1)]
    max_streak_profit_upto_i = [last_streak_profit]
    for i in range(num_streaks - 2, -1, -1):
        max_profit_upto_ith_streak_pair = max_profit_streak_pairs_upto_streak_i[-1]
        max_profit_upto_ith_streak = max_streak_profit_upto_i[-1]
        if (
            prices[streaks[i][0]]
            < prices[streaks[max_profit_upto_ith_streak_pair[0]][0]]
        ):
            max_profit_upto_ith_streak = (
                prices[streaks[max_profit_upto_ith_streak_pair[1]][1]]
                - prices[streaks[i][0]]
            )
            max_profit_upto_ith_streak_pair = (
                i,
                max_profit_upto_ith_streak_pair[1],
            )
        if prices[streaks[i][1]] - prices[streaks[i][0]] > max_profit_upto_ith_streak:
            max_profit_upto_ith_streak_pair = (i, i)
            max_profit_upto_ith_streak = prices[streaks[i][1]] - prices[streaks[i][0]]
        max_profit_streak_pairs_upto_streak_i.append(max_profit_upto_ith_streak_pair)
        max_streak_profit_upto_i.append(max_profit_upto_ith_streak)
    return max_profit_streak_pairs_upto_streak_i, max_streak_profit_upto_i


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        streaks = find_streaks_of_increasing_prices(prices)
        print(
            f"After processing all costs: streaks = {[f'{streak[0]}={prices[streak[0]]}, {streak[1]}={prices[streak[1]]}' for streak in streaks]}"
        )

        # early exit path
        num_streaks = len(streaks)
        if not streaks:
            return 0
        first_streak_profit = prices[streaks[0][1]] - prices[streaks[0][0]]
        if num_streaks == 1:
            return first_streak_profit

        _, max_profit_upto_ith_streak_from_first_streak_onwards = (
            find_max_profit_upto_ith_streak_from_first_streak(prices, streaks)
        )
        _, max_streak_profit_upto_ith_streak_from_last_streak_onwards = (
            find_max_streak_profit_upto_ith_streak_from_last_streak(prices, streaks)
        )

        # print(f"max_profit_streak_pairs_upto_streak_i_from_left={max_profit_streak_pairs_upto_streak_i_from_left}")
        print(
            f"max_profit_upto_ith_streak_from_first_streak_onwards={max_profit_upto_ith_streak_from_first_streak_onwards}"
        )
        # print(f"max_profit_streak_pairs_upto_streak_i_from_right={max_profit_streak_pairs_upto_streak_i_from_right}")
        print(
            f"max_streak_profit_upto_ith_streak_from_last_streak_onwards={max_streak_profit_upto_ith_streak_from_last_streak_onwards}"
        )

        return max(
            max(
                max_profit_upto_ith_streak_from_first_streak_onwards[i]
                + max_streak_profit_upto_ith_streak_from_last_streak_onwards[
                    num_streaks - 2 - i
                ]
                for i in range(num_streaks - 1)
            ),
            max_profit_upto_ith_streak_from_first_streak_onwards[num_streaks - 1],
        )
"""


def find_max_profit_upto_i_from_first(prices: list[int]) -> list[int]:
    n = len(prices)
    ret = [0]
    global_min_price = prices[0]
    for i in range(1, n):
        price = prices[i]
        profit = max(ret[-1], price - global_min_price)
        global_min_price = min(global_min_price, price)
        ret.append(profit)
    return ret


def find_max_profit_upto_i_from_last(prices: list[int]) -> list[int]:
    n = len(prices)
    ret = [0]
    global_max_price = prices[n - 1]
    for i in range(n - 2, 0, -1):
        price = prices[i]
        profit = max(ret[-1], global_max_price - price)
        global_max_price = max(global_max_price, price)
        ret.append(profit)
    return ret


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        # # functional TC=SC=O(n) approach.
        # if not prices:
        #     return 0
        # n = len(prices)
        # if n == 1:
        #     return 0
        # max_profit_upto_i_from_first = find_max_profit_upto_i_from_first(prices)
        # max_profit_upto_i_from_last = find_max_profit_upto_i_from_last(prices)
        # return max(
        #     max(
        #         max_profit_upto_i_from_first[i] + max_profit_upto_i_from_last[n - 2 - i]
        #         for i in range(n - 1)
        #     ),
        #     max_profit_upto_i_from_first[n - 1],
        # )

        # Alternative TC=O(n), SC=O(1) approach.
        buy1: float | int = float("-inf")
        sell1: float | int = 0
        buy2: float | int = float("-inf")
        sell2: float | int = 0
        for price in prices:
            buy1 = max(buy1, -price)
            sell1 = max(sell1, buy1 + price)
            buy2 = max(buy2, sell1 - price)
            sell2 = max(sell2, buy2 + price)
        return int(sell2)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(prices: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maxProfit(prices)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(prices=[1, 5, 2, 7, 4, 8, 1, 10], expected=16)
            Test(prices=[], expected=0)
            Test(prices=[1], expected=0)
            Test(prices=[3, 3, 5, 0, 0, 3, 1, 4], expected=6)
            Test(prices=[7, 6, 4, 3, 1], expected=0)
            Test(prices=[1, 2, 4, 2, 5, 7, 2, 4, 9, 0], expected=13)
            Test(prices=[0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8], expected=8)
            Test(
                prices=[3, 5, 3, 5, 3, 7, 1, 6, 2, 7, 3, 4, 3, 5, 3, 4, 3, 7],
                expected=10,
            )
            Test(prices=[1, 3, 5, 4, 3, 7, 6, 9, 2, 4], expected=10)
            Test(prices=[8, 3, 6, 2, 8, 8, 8, 4, 2, 0, 7, 2, 9, 4, 9], expected=15)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
