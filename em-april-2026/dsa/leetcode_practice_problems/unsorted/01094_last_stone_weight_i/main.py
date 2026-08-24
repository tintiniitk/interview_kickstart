DEBUGGING = False
if DEBUGGING:
    LEVEL: int = 1
    SEQ: list[int] = []


class Solution:
    def lastStoneWeightII(self, stones: list[int]) -> int:
        # My O(2^n) solution
        # Remove all 0s as they are inconsequential.
        stones = list(filter(lambda x: x != 0, stones))
        # The problem essentially reduces to find the minimum of difference of sums of any of pair of complementary subset of stones.
        # e.g. numbers are {a,b,c} then one pair is ({a},{b,c}) and their difference of sums is abs(a-(b+c)).
        # Similarly we need to find and return the minima these sums of differences of different splits of nums array.
        # This also simplifies to finding the closest sum of any subset of the nums array to half of sum of entire array, and return twice of the delta.
        # i.e. nums = {a,b,c}, and s=a+b+c. Then we need to find the subset of nums whose sum is closest to s/2 say X, then we need to return 2*(s/2-X) or s - 2*X.
        half = sum(stones) / 2.0

        """
        n = len(stones)
        # Sort the stones to make pruning of branches more effective.
        stones.sort()
        # Find the individual number closes to half.
        min_gap_from_half = min(abs(stone - half) for stone in stones)
        if (
            min_gap_from_half <= 0.5
        ):  # if min_gap_from_half is half, it means the total sum is odd, then min_gap_from_half is absolute minimum possible. If min_gap_from_half is 0, then it means we have found half in the array itself.
            return int(2 * min_gap_from_half)
        if DEBUGGING:
            print(
                f"Initially, stones={stones}, half={half}, min_gap_from_half={min_gap_from_half}"
            )

        def helper(i: int, ssf: int) -> bool:
            nonlocal min_gap_from_half
            if DEBUGGING:
                nonlocal LEVEL
                nonlocal SEQ
            if DEBUGGING:
                print(f"{'    ' * LEVEL}helper(SEQ={SEQ}), ssf={ssf}, i={i}")
            abs_ssf = abs(ssf - half)
            if abs_ssf < min_gap_from_half:  # we have found a better subset.
                min_gap_from_half = abs_ssf
                if DEBUGGING:
                    print(
                        f"{'    ' * (LEVEL + 1)}**************************** min_gap_from_half = {abs_ssf}"
                    )
                if (
                    min_gap_from_half <= 0.5
                ):  # if min_gap_from_half is half, it means the total sum is odd, then min_gap_from_half is absolute minimum possible. If min_gap_from_half is 0, then it means we have found the perfect split.
                    return True
            if i == n:  # exhausted the entire set of stones. Closing this branch.
                return False
            val = stones[i]
            if i == 0:
                # include [i]
                if DEBUGGING:
                    LEVEL += 1
                    SEQ.append(val)
                if helper(i + 1, ssf + val):
                    return True
                if DEBUGGING:
                    LEVEL -= 1
                    SEQ.pop()
                # exclude [i]
                if DEBUGGING:
                    LEVEL += 1
                if helper(i + 1, ssf):
                    return True
                if DEBUGGING:
                    LEVEL -= 1
            else:
                # include [i]
                if DEBUGGING:
                    LEVEL += 1
                    SEQ.append(val)
                if ssf + val < half + min_gap_from_half and helper(i + 1, ssf + val):
                    return True
                if DEBUGGING:
                    LEVEL -= 1
                    SEQ.pop()
                # exclude [i]
                if DEBUGGING:
                    LEVEL += 1
                if (
                    i < n - 1
                    and ssf + (n - i - 1) * (stones[-1]) > half - min_gap_from_half
                    and ssf + stones[i + 1] < half + min_gap_from_half
                    and helper(i + 1, ssf)
                ):
                    return True
                if DEBUGGING:
                    LEVEL -= 1
            return False

        if DEBUGGING:
            LEVEL = 1
            SEQ = []
        helper(i=0, ssf=0)
        return int(2 * min_gap_from_half)
        """

        # Optimal O(n*sum) solution.
        target = int(half)
        # print(f"target = {target}")
        dp = [False] * (target + 1)  # dp[i] is true if the sum i is possible.
        dp[0] = True
        for stone in stones:
            # loop backwards to avoid reusing a stone.
            for j in range(target, stone - 1, -1):
                if dp[j - stone]:
                    dp[j] = True
        # print(f"dp = { {i: val for i, val in enumerate(dp)} }")
        for s in range(target, 0, -1):
            if dp[s]:
                return int(2 * (half - s))
        return int(half * 2)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(stones: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().lastStoneWeightII(stones)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(stones=[2, 7, 4, 1, 8, 1], expected=1)
            Test(stones=[31, 26, 33, 21, 40], expected=5)
            Test(stones=[2, 4, 5, 6, 7, 8, 8], expected=0)
            Test(
                stones=[
                    89,
                    23,
                    100,
                    93,
                    82,
                    98,
                    91,
                    85,
                    33,
                    95,
                    72,
                    98,
                    63,
                    46,
                    17,
                    91,
                    92,
                    72,
                    77,
                    79,
                    99,
                    96,
                    55,
                    72,
                    24,
                    98,
                    79,
                    93,
                    88,
                    92,
                ],
                expected=0,
            )
            Test(stones=[1, 2], expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
