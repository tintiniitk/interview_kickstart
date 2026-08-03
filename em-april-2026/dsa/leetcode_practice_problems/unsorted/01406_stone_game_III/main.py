from typing import List

class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        if n == 1:
            return "Alice" if stoneValue[0] > 0 else "Bob" if stoneValue[0] < 0 else "Tie"
        sum_stoneValue_by_2 = sum(stoneValue) / 2
        dp = [0 for _ in range(n+1)] # dp[i] = max score Alice can get if they have to choose from stoneValue[i:]
        for i in range(n-1, -1, -1):
            dp[i] = stoneValue[i] + (min(dp[i+2], dp[i+3], dp[i+4]) if i <= n-4 else min(dp[i+2], dp[i+3]) if i <= n-3 else dp[i+2] if i <= n-2 else 0)
            if i < n-1:
                dp[i] = max(dp[i], stoneValue[i] + stoneValue[i+1] + (min(dp[i+3], dp[i+4], dp[i+5]) if i <= n-5 else min(dp[i+3], dp[i+4]) if i <= n-4 else dp[i+3] if i <= n-3 else 0))
                if i < n-2:
                    dp[i] = max(dp[i], stoneValue[i] + stoneValue[i+1] + stoneValue[i+2] + (min(dp[i+4], dp[i+5], dp[i+6]) if i <= n-6 else min(dp[i+4], dp[i+5]) if i <= n-5 else dp[i+4] if i <= n-4 else 0))
        return "Alice" if dp[0] > sum_stoneValue_by_2 else "Bob" if dp[0] < sum_stoneValue_by_2 else "Tie"

def Test(stoneValue, expected):
    s = Solution()
    result = s.stoneGameIII(stoneValue)
    assert result == expected, f"Expected {expected}, but got {result}"

Test([1, 2, 3, 7], "Bob")
Test([1, 2, 3, -9], "Alice")
Test([1, 2, 3, 6], "Tie")