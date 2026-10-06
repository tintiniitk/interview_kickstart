def pattern_matcher(text: str, pattern: str) -> bool:
    """
    Args:
     text(str)
     pattern(str)
    Returns:
     bool
    """
    n = len(text)
    p = len(pattern)
    dp = [[False for _ in range(p + 1)] for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        dp[i][0] = False
    for j in range(2, p + 1):
        dp[0][j] = j % 2 == 0 and dp[0][j - 2] and pattern[j - 1] == "*"
    for i in range(1, n + 1):
        for j in range(1, p + 1):
            dp[i][j] = (
                (
                    dp[i - 1][j]
                    and pattern[j - 1] == "*"
                    and pattern[j - 2] in {".", text[i - 1]}
                )
                or (
                    dp[i][j - 1]
                    and pattern[j - 1] == "*"
                    and pattern[j - 2] in {".", text[i - 1]}
                )
                or (dp[i - 1][j - 1] and (pattern[j - 1] in {".", text[i - 1]}))
                or (p >= 2 and dp[i][j - 2] and pattern[j - 1] == "*")
            )
            # print(
            #     f"dp[{i:02}][{j:02}] = regex_match({text[:i]},{pattern[:j]}) = {dp[i][j]}"
            # )

    return dp[n][p]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=True)
def Test(text: str, pattern: str, expected: bool) -> tuple[bool, str]:
    actual = pattern_matcher(text, pattern)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc
from tc_y import tc as tc_y_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(text="abbbc", pattern="ab*c", expected=True)
            Test(text="abc", pattern=".ab*..", expected=False)
            Test(text="aa", pattern="a*.", expected=True)
            Test(text="ab", pattern="a*.", expected=True)
            Test(text="b", pattern="a*.", expected=True)
            Test(text="abcdefg", pattern="a.c.*.*gg*", expected=True)
            Test(text="aaa", pattern=".a*..", expected=True)
            Test(text="abcdefghijk", pattern="...........*kl*z*a*", expected=True)
            Test(text="abcdefg", pattern="abcc*d*e*e*ee*fg*.", expected=True)
            Test(text="abccccdefg", pattern="abccc*.de.g*g", expected=True)
            Test(text="abchijxyhijaak", pattern="abc.*hij.*hija*k", expected=True)
            Test(
                text="abchhhhhijxyhijaahijk",
                pattern="abc.*hhhij.*hijk.*",
                expected=True,
            )
            Test(**tc_x_tc)
            Test(
                text="aaaaaaa",
                pattern="..*..*..*..*..*..*..*",
                expected=True,
            )
            Test(**tc_y_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
