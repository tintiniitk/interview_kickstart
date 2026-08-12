class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        if not p:
            if not s:
                return True
            else:
                return False
        n = len(s)
        m = len(p)
        print(f"n={n}, m={m}, s='{s}', p='{p}'")

        # # DP solution with TC=O(mn), SC(m)
        # dp = [[False for _ in range(m + 1)] for _ in range(n + 1)]
        # dp[0][0] = True  # default
        # for j in range(1, m + 1):
        #     dp[0][j] = dp[0][j - 1] and p[j - 1] == "*"
        # for i in range(1, n + 1):
        #     dp[i % 2][0] = False
        #     for j in range(1, m + 1):
        #         if p[j - 1] == "*":
        #             value = (
        #                 dp[i % 2][j - 1] or dp[(i - 1) % 2][j - 1] or dp[(i - 1) % 2][j]
        #             )
        #             dp[i % 2][j] = value
        #         elif p[j - 1] == "?":
        #             value = dp[(i - 1) % 2][j - 1]
        #             dp[i % 2][j] = value
        #         else:
        #             value = dp[(i - 1) % 2][j - 1] and p[j - 1] == s[i - 1]
        #             dp[i % 2][j] = value
        # return dp[n % 2][m]

        # DFS solution with TC=O(mn), SC(1)
        si, pi = 0, 0
        star, match = -1, -1  # where s[:i]===p[:j]
        while True:
            # print(f"si={si}, pi={pi}, star={star},match={match}")
            if si == n:
                if pi == m:
                    return True
                if pi < m:
                    if p[pi] == "*":
                        pi += 1
                        continue
                    else:
                        return False
            elif pi < m:
                pattern_char = p[pi]
                if pattern_char != "*":
                    if pattern_char == "?" or s[si] == pattern_char:
                        si += 1
                        pi += 1
                        continue
                    elif star != -1:
                        pi = star + 1
                        match += 1
                        si = match
                    else:
                        return False
                else:
                    star = pi
                    match = si
                    pi += 1
            else:
                if star != -1:
                    pi = star + 1
                    match += 1
                    si = match
                else:
                    return False
        return si == n and pi == m


def Test(s: str, p: str, expected: bool):
    orig_s = "".join(s)
    orig_p = "".join(p)
    print(f"[RUN]")
    actual = Solution().isMatch(s, p)
    assert (
        actual == expected
    ), f"  actual(={actual}) != expected(={expected}) for s='{orig_s}', p='{orig_p}'\n[FAILED]"
    print(f"[DONE] for s='{orig_s}', p='{orig_p}'")


Test("", "", True)
Test("", "******", True)
Test("abc", "abc", True)
Test("abc", "a?c", True)
Test("abc", "a*", True)
Test("abc", "*", True)
Test("abc", "*c", True)
Test("abc", "*bc", True)
Test("abc", "a*bc", True)
Test("abc", "a?bc", False)
Test("abc", "ac*", False)
Test("abcd", "a*", True)
Test("abcd", "a*?", True)
Test("abcd", "a*??", True)
Test("abcd", "a*???", True)
Test("abcd", "a*????", False)
Test("abcd", "????", True)
Test("ab", "*?*", True)
Test("a", "*?*", True)
Test("abcehifheoigiro", "*?*", True)
Test("abcd", "a?c*", True)
Test("abcd", "a??c*", False)
Test("bbbaab", "a**?***", False)
