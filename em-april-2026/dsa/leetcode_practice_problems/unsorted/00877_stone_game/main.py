class Solution:
    def stoneGame(self, piles: list[int]) -> bool:
        n = len(piles)
        if n == 2:
            return True
        n_by_2 = n // 2
        dp = [[0 for _ in range(n_by_2 + 1)] for _ in range(n)]
        # print(dp)
        for size_by_2 in range(1, n_by_2 + 1):
            # print(f"  at size_by_2={size_by_2}")
            for i in range(n - 2 * size_by_2 + 1):
                j = i + 2 * size_by_2
                # print(f"  at size_by_2={size_by_2}, i={i}, j ={j}")
                if size_by_2 == 1:
                    dp[i][size_by_2] = max(piles[i], piles[j - 1])
                else:
                    a = piles[i] + min(
                        dp[i + 1][size_by_2 - 1], dp[i + 2][size_by_2 - 1]
                    )
                    b = piles[j - 1] + min(
                        dp[i + 1][size_by_2 - 1], dp[i][size_by_2 - 1]
                    )
                    dp[i][size_by_2] = max(a, b)

        return dp[0][n_by_2] > (sum(piles) // 2)


def Test(piles, expected):
    s = Solution()
    result = s.stoneGame(piles)
    assert result == expected, f"Expected {expected}, but got {result}"


Test([5, 3, 4, 5], True)
Test([3, 7, 2, 3], True)
