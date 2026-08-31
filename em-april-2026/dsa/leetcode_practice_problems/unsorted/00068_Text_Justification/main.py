from itertools import accumulate


class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        n = len(words)
        lens = list(map(len, words))
        cumu_lens = [0] + list(accumulate(lens))
        # print(f"maxWidth={maxWidth}, words={words}, lens={lens}, cumu_lens = {cumu_lens}")

        ret = []

        def consumed_words_justified(start: int, end: int, is_last_line: bool) -> str:
            nonlocal ret
            total_length = cumu_lens[end] - cumu_lens[start]
            num_words = end - start
            total_spaces = maxWidth - total_length
            if not is_last_line:
                if num_words == 1:
                    return words[start] + "".join([" "] * (maxWidth - (lens[start])))
                num_gaps = num_words - 1
                if total_spaces % num_gaps == 0:
                    num_spaces_per_gap = total_spaces // num_gaps
                    spaces_per_gap = "".join(" " * num_spaces_per_gap)
                    return spaces_per_gap.join(words[start:end])
                else:
                    num_spaces_per_later_gap = total_spaces // num_gaps
                    num_spaces_per_initial_gap = num_spaces_per_later_gap + 1
                    num_initial_gaps = total_spaces % num_gaps
                    spaces_per_initial_gap = "".join(" " * num_spaces_per_initial_gap)
                    spaces_per_later_gap = "".join(" " * num_spaces_per_later_gap)
                    return (
                        spaces_per_initial_gap.join(
                            words[start : start + num_initial_gaps + 1]
                        )
                        + spaces_per_later_gap
                        + spaces_per_later_gap.join(
                            words[start + num_initial_gaps + 1 : end]
                        )
                    )
            else:
                return " ".join(words[start:end]) + "".join(
                    [" "]
                    * (
                        maxWidth
                        - (cumu_lens[end] - cumu_lens[start])
                        - (end - start - 1)
                    )
                )

        consumed_words = 0
        while consumed_words < n:
            # print(f"new loop iteration with consumed_words={consumed_words}, i={consumed_words+1}")
            i = consumed_words + 1
            if consumed_words < n - 1:
                while (
                    i <= n
                    and cumu_lens[i]
                    - cumu_lens[consumed_words]
                    + (i - consumed_words - 1)
                    <= maxWidth
                ):
                    i += 1
                i -= 1
            # print(f"calling consumed_words_justified(start={consumed_words}, end={i}, {i==n})")
            ret += [consumed_words_justified(consumed_words, i, i == n)]
            # print(f"ret={ret}")
            consumed_words = i
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(words: list[str], maxWidth: int, expected: list[str]) -> tuple[bool, str]:
    actual = Solution().fullJustify(words, maxWidth)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                words=["This", "is", "an", "example", "of", "text", "justification."],
                maxWidth=16,
                expected=["This    is    an", "example  of text", "justification.  "],
            )
            Test(
                words=["What", "must", "be", "acknowledgment", "shall", "be"],
                maxWidth=16,
                expected=["What   must   be", "acknowledgment  ", "shall be        "],
            )
            Test(
                words=[
                    "Science",
                    "is",
                    "what",
                    "we",
                    "understand",
                    "well",
                    "enough",
                    "to",
                    "explain",
                    "to",
                    "a",
                    "computer.",
                    "Art",
                    "is",
                    "everything",
                    "else",
                    "we",
                    "do",
                ],
                maxWidth=20,
                expected=[
                    "Science  is  what we",
                    "understand      well",
                    "enough to explain to",
                    "a  computer.  Art is",
                    "everything  else  we",
                    "do                  ",
                ],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
