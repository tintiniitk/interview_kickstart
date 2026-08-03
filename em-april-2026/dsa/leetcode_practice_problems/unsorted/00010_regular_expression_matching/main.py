class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """ define groups from pattern p.
        Groups are (a) individual alphabet or a string of alphabets e.g. 'a' or 'abcd', (b) an alphabet followed by *
        e.g. 'a*', or 'b*', (c) just a dot i.e. '.', or (d) dot followed by a start i.e. '.*'
        To create the groups, p is scanned in reverse order for ease of bookkeeping.
        """
        groups = list[str]()
        len_p = len(p)
        p_rev = list(reversed(p))
        for i, char in enumerate(p_rev):
            if char == "*":
                # if i < len_p -1 and p_rev[i-1] == '*':
                #     raise ValueError(f"** not allowed in pattern, . groups created so far = {list(reversed(groups))} from pattern processed = {p[len_p-i:]}")
                # if i == len_p - 1:
                #     raise ValueError(f"* not allowed in the beginning of the pattern. groups created so far = {list(reversed(groups))} from pattern processed = {p[len_p-i:]}")
                groups.append(char)
            elif char == ".":
                if groups and groups[-1] == "*":
                    groups[-1] = char + groups[-1]
                else:
                    groups.append(char)
            else:
                if groups and (
                    groups[-1] == "*"
                    or (groups[-1].count(".") == 0 and groups[-1].count("*") == 0)
                ):
                    groups[-1] = char + groups[-1]
                else:
                    groups.append(char)
        groups.reverse()
        # print(f"groups={groups}")

        n = len(s)
        g = len(groups)
        """ Create 2-d dp array dp[i][j] which stores True if s[:j] matches p[:i]."""
        dp = [[False for _ in range(n + 1)] for _ in range(g + 1)]
        # by definition, empty string s[:0] matches empty-pattern p[:0].
        dp[0][0] = True
        for g in range(1, g + 1):
            group = groups[g - 1]
            # all those patterns match empty string "" which only have groups ending with * in them, e.g. 'a*', or 'a*b*' or 'a*.*b*' etc.
            dp[g][0] = dp[g - 1][0] and group[-1] == "*"
            for c in range(1, n + 1):
                char = s[c - 1]
                # find if the current character in target string s matches the current group in the pattern.
                dp[g][c] = dp[g - 1][c - 1] and (group in {".", ".*", char, char + "*"})
                dp[g][c] |= dp[g - 1][c] and group[-1] == "*"
                dp[g][c] |= any(
                    [
                        (
                            c > (k - 1)
                            and dp[g - 1][c - k]
                            and (
                                group in {s[c - k : c], ".*"}
                                or (
                                    group == s[c - k] + "*"
                                    and all(
                                        [s[c - k + j] == s[c - k] for j in range(1, k)]
                                    )
                                )
                            )
                        )
                        for k in range(2, 21)
                    ]
                )
                dp[g][c] |= dp[g][c - 1] and (
                    group == ".*"
                    or any(
                        [
                            (
                                c > k - 1
                                and group == s[c - k] + "*"
                                and all([s[c - k + j] == s[c - k] for j in range(1, k)])
                            )
                            for k in range(1, 21)
                        ]
                    )
                )
                # if dp[g][c]:
                #     print(f"{s[:c]} matches {"".join(groups[:g])}")
        return dp[g][n]


def Test(s: str, p: str, expected: bool):
    actual = Solution().isMatch(s, p)
    assert actual == expected, f"got {actual}, expected {actual} for s='{s}', p='{p}'"


Test("abcd", "ab*cd", True)
Test("abcd", "a.*.b*cd", True)
Test("abcd", "a.*.*.*.b*cd", True)
Test("ab", "a.", True)
Test("ab", "ab", True)
Test("ab", "..", True)
Test("ab", "a.*", True)
Test("ab", ".*b", True)
Test("abc", ".bc", True)
Test("abcd", ".bcd", True)
Test("aa", "a", False)
Test("aa", "a*", True)
Test("ab", ".*", True)
Test("abcdefghijklmnopqrst", "abcdefghijklmnopqrst", True)
Test("abcdefghijklmnopqrst", "a*c*.*d*t", True)
Test("mississippi", "mis*is*p*.", False)
Test("abcdefghijklmnop", "ab*op", False)
Test("abbbbbbbbbbbbbbop", "ab*op", True)
Test("", "", True)
Test("", "a*", True)
Test("", "a*b*", True)
Test("", "a*.*b*", True)
Test("abcdefghijklmnopqrst", "abcdefghijklmnopqrst", True)
Test("abcdefghijklmnopqrst", "a.c.*fg...*l.no.q.s.", True)
