from functools import cache
from itertools import combinations
from math import lcm as lcm2


class Solution:
    def findKthSmallest(self, coins: list[int], k: int) -> int:
        # edge cases
        n = len(coins)
        if n == 1:
            return k * coins[0]
        coins.sort()
        if k == 1:
            return coins[0]
        # remove dependent coins
        surviving_coins = [coins[0]]
        for coin in coins[1:]:
            if all(coin % surviving_coin != 0 for surviving_coin in surviving_coins):
                surviving_coins.append(coin)
        coins = surviving_coins
        n = len(coins)
        if n == 1:
            return k * coins[0]

        # find max-possible values of k-th smallest value.
        min_val, max_val = coins[0], coins[0] * k

        # find LCMs of odd and even sizes subsets of the coins.
        # [0] are the LCMs of the odd-sized subsets of coins array.
        # [1] are the LCMs of the even-sized subsets of coins array.
        # [0] and [1] can contain duplicates. This is on purpose to
        # account for two distinct subsets having the same LCM.
        lcms = [coins.copy(), []]
        for size in range(2, n + 1):
            lcms_arr = lcms[(size + 1) % 2]
            for combination in combinations(coins, size):
                if any(num > max_val for num in combination):
                    continue
                lcm_value = lcm2(*combination)
                if lcm_value > max_val:
                    continue
                lcms_arr.append(lcm_value)

        @cache
        def rank(val: int) -> int:
            """Find rank of the given numbers with the given LCM 2d vectors"""
            r = 0
            for lcm_value in lcms[0]:
                r += val // lcm_value
            for lcm_value in lcms[1]:
                r -= val // lcm_value
            return r

        # Eventually when we find a number M such that its rank is k, then
        # we need to also ensure that we need to return the actual
        # k-th number which is a multiple of at least one of the coins.
        # For that, we need to find the greatest number less than or equal
        # to M which is divisible by any of the coins.
        # We don't need to worry about the scale as the search-space won't be
        # more than the value of the smallest coin i.e. coins[0] .
        def find_less_or_equal_valid_multiple_of_any_coin(val: int) -> int:
            while val >= coins[0]:
                if any(val % coin == 0 for coin in coins):
                    return val
                val -= 1
            raise ValueError(
                f"Unexpected scenario, couldn't find find_less_or_equal_valid_multiple_of_any_coin({val})"
            )

        num_iter = 0  # purely for debugging.
        found_val = -1
        while min_val <= max_val:
            num_iter += 1
            if min_val == max_val:
                if rank(min_val) == k:
                    found_val = min_val
                    break
                else:
                    raise ValueError(f"Unexpected scenario, couldn't find rank k={k}")
            elif max_val - min_val == 1:
                if rank(max_val) == k:
                    found_val = max_val
                    break
                elif rank(min_val) == k:
                    found_val = min_val
                    break
                else:
                    raise ValueError(f"Unexpected scenario, couldn't find rank k={k}")
            else:
                mid = (min_val + max_val) // 2
                mid_rank = rank(mid)
                if k == mid_rank:
                    found_val = mid
                    break
                elif k < mid_rank:
                    max_val = mid - 1
                else:
                    min_val = mid + 1
        if found_val != -1:
            return find_less_or_equal_valid_multiple_of_any_coin(found_val)
        raise ValueError(f"Unexpected scenario, couldn't find rank k={k}")


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(coins: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().findKthSmallest(coins, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(coins=[20, 6, 15, 16, 22], k=25727, expected=88434)
            Test(coins=[3, 6, 9], k=3, expected=9)
            Test(coins=[5, 2], k=7, expected=12)
            Test(coins=[3, 5, 2], k=5, expected=6)
            Test(coins=[9, 10, 7, 3], k=1, expected=3)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
