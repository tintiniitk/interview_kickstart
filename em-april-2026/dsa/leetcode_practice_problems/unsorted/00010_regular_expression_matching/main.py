class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """define groups from pattern p.
        Groups are (a) individual alphabet or a string of alphabets e.g. 'a' or 'abcd', (b) an alphabet followed by *
        e.g. 'a*', or 'b*', (c) just a dot i.e. '.', or (d) dot followed by a start i.e. '.*'
        To create the groups, p is scanned in reverse order for ease of bookkeeping.
        """
        groups = list[str]()
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
        for gi in range(1, g + 1):
            group = groups[gi - 1]
            # all those patterns match empty string "" which only have groups ending with * in them, e.g. 'a*', or 'a*b*' or 'a*.*b*' etc.
            dp[gi][0] = dp[gi - 1][0] and group[-1] == "*"
            for c in range(1, n + 1):
                char = s[c - 1]
                # find if the current character in target string s matches the current group in the pattern.
                dp[gi][c] = dp[gi - 1][c - 1] and (
                    group in {".", ".*", char, char + "*"}
                )
                dp[gi][c] |= dp[gi - 1][c] and group[-1] == "*"
                dp[gi][c] |= any(
                    (
                        c > (k - 1)
                        and dp[gi - 1][c - k]
                        and (
                            group in {s[c - k : c], ".*"}
                            or (
                                group == s[c - k] + "*"
                                and all(s[c - k + j] == s[c - k] for j in range(1, k))
                            )
                        )
                    )
                    for k in range(2, 21)
                )
                dp[gi][c] |= dp[gi][c - 1] and (
                    group == ".*"
                    or any(
                        (
                            c > k - 1
                            and group == s[c - k] + "*"
                            and all(s[c - k + j] == s[c - k] for j in range(1, k))
                        )
                        for k in range(1, 21)
                    )
                )
                # if dp[gi][c]:
                #     print(f"{s[:c]} matches {"".join(groups[:gi])}")
        return dp[g][n]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, p: str, expected: bool) -> tuple[bool, str]:
    actual = Solution().isMatch(s, p)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="abcd", p="ab*cd", expected=True)
            Test(s="abcd", p="a.*.b*cd", expected=True)
            Test(s="abcd", p="a.*.*.*.b*cd", expected=True)
            Test(s="ab", p="a.", expected=True)
            Test(s="ab", p="ab", expected=True)
            Test(s="ab", p="..", expected=True)
            Test(s="ab", p="a.*", expected=True)
            Test(s="ab", p=".*b", expected=True)
            Test(s="abc", p=".bc", expected=True)
            Test(s="abcd", p=".bcd", expected=True)
            Test(s="aa", p="a", expected=False)
            Test(s="aa", p="a*", expected=True)
            Test(s="ab", p=".*", expected=True)
            Test(s="abcdefghijklmnopqrst", p="abcdefghijklmnopqrst", expected=True)
            Test(s="abcdefghijklmnopqrst", p="a*c*.*d*t", expected=True)
            Test(s="mississippi", p="mis*is*p*.", expected=False)
            Test(s="abcdefghijklmnop", p="ab*op", expected=False)
            Test(s="abbbbbbbbbbbbbbop", p="ab*op", expected=True)
            Test(s="", p="", expected=True)
            Test(s="", p="a*", expected=True)
            Test(s="", p="a*b*", expected=True)
            Test(s="", p="a*.*b*", expected=True)
            Test(s="abcdefghijklmnopqrst", p="abcdefghijklmnopqrst", expected=True)
            Test(s="abcdefghijklmnopqrst", p="a.c.*fg...*l.no.q.s.", expected=True)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
