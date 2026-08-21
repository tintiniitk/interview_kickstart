class Solution:
    def expressiveWords(self, s: str, words: list[str]) -> int:
        def repr(input: str):
            if not input:
                return []
            ret = [[input[0], 1]]
            l = len(input)
            for i in range(1, l):
                c = input[i]
                if c == ret[-1][0]:
                    ret[-1][1] += 1
                else:
                    ret.append([c, 1])
            return ret

        def is_stretchy(q_repr, s_repr):
            if len(q_repr) != len(s_repr):
                return False
            for i in range(len(q_repr)):
                if q_repr[i][0] != s_repr[i][0] or (
                    q_repr[i][1] != s_repr[i][1]
                    and (q_repr[i][1] > s_repr[i][1] or s_repr[i][1] < 3)
                ):
                    return False
            return True

        s_repr = repr(s)
        return len(list(filter(lambda q: is_stretchy(repr(q), s_repr), words)))


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.05, stop_on_tc_failure=False)
def Test(s: str, words: list[str], expected: int):
    actual = Solution().expressiveWords(s, words)
    if actual != expected:
        return False, f"got={truncate_param(actual)}, wanted={truncate_param(expected)}"
    return True, ""


def main():
    try:
        with time_limit(5):
            Test(s="heeellooo", words=["hello", "hi", "helo"], expected=1)
            Test(s="zzzzzyyyyy", words=["zzyy", "zy", "zyy"], expected=3)
    except TimeoutException as te:
        print(f"Tests run timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
