import logging

# CONFIGURE LOGGING LEVEL DYNAMICALLY
# If DEBUG_MODE is True, the logger captures everything down to DEBUG.
# If False, it defaults to INFO, ignoring debug statements.
# log_level = logging.DEBUG
log_level = logging.INFO
logging.basicConfig(
    level=log_level,
    # format="%(asctime)s - [%(levelname)s] - %(message)s"
    format="[%(levelname)s] %(message)s",
)
# CREATE A LOGGER INSTANCE
logger = logging.getLogger(__name__)

from collections import defaultdict

"""
# A less efficient approach.
class Solution:
    def findSubstring(self, s: str, words: list[str]) -> list[int]:
        if not s:
            return []
        n = len(s)
        k = len(words)
        m = len(words[0])
        if k * m > n:
            return []

        logger.debug(f"findSubstring({s}, {words})")

        word_frequency_map = defaultdict(int)
        for word in words:
            word_frequency_map[word] += 1

        char_frequency_map = defaultdict(int)
        for word in words:
            for char in word:
                char_frequency_map[char] += 1

        logger.debug(f"  word_frequency_map={word_frequency_map}, char_frequency_map={char_frequency_map}")

        frequency_checker = defaultdict(int)
        def reset_frequency_checker():
            nonlocal frequency_checker
            frequency_checker = word_frequency_map.copy()
        def check_word_in_frequency_checker(word: str) -> bool:
            nonlocal frequency_checker
            if word not in frequency_checker or frequency_checker[word] < 1:
                return False
            frequency_checker[word] -= 1
            return True
        def check_word_frequency_checker() -> bool:
            for word, freq in frequency_checker.items():
                if freq != 0:
                    return False
            return True

        char_frequency_checker = defaultdict(int)
        def check_char_frequency_checker() -> bool:
            for char, freq in char_frequency_checker.items():
                if freq != 0 and freq != char_frequency_map[char]:
                    return False
            return True

        # output_state
        output_indexes = []

        w = k * m # window-size = sum of length of all words in words array.
        # populate char_frequency_checker separately for i=0.
        i = 0
        for j in range(i, i + w):
            char = s[j]
            char_frequency_checker[s[j]] += 1

        for i in range(n - w + 1):
            qualifies = True
            reset_frequency_checker()
            if i > 0: # slide the window
                char_frequency_checker[s[i+w-1]] += 1
                char_frequency_checker[s[i-1]] -= 1
            if check_char_frequency_checker():
                logger.debug(f"    at i={i}, char-freq matched, going to check word-frequency ...")
                for j in range(i, i + w, m):
                    word = s[j:j+m]
                    if not check_word_in_frequency_checker(word):
                        logger.debug(f"    at i={i}, {word} not found in frequency_checker={frequency_checker}")
                        qualifies = False
                        break
                if qualifies:
                    if not check_word_frequency_checker():
                        logger.debug(f"    at i={i}, after checking all words, {frequency_checker} is not all zeroes, so i={i} abandoned")
                        qualifies = False
                    else:
                        logger.debug(f"    at i={i}, word-freq matched, so going to accept as an answer")
                        pass
            else:
                logger.debug(f"    at i={i}, char-freq did not match so abandoned")
                qualifies = False
            if qualifies:
                output_indexes.append(i)
        return output_indexes
"""


class Solution:
    def findSubstring(self, s: str, words: list[str]) -> list[int]:
        if not s:
            return []
        n = len(s)
        num_words = len(words)
        m = len(words[0])
        w = num_words * m  # window-size = sum of length of all words in words array.
        if w > n:
            return []
        logger.debug(f"findSubstring({s}, {words})")

        word_frequency_map = defaultdict(int)
        for word in words:
            word_frequency_map[word] += 1
        logger.debug(f"  word_frequency_map={word_frequency_map}")

        frequency_checker = defaultdict(int)

        def reset_frequency_checker():
            nonlocal frequency_checker
            frequency_checker = word_frequency_map.copy()

        def check_word_in_frequency_checker(word: str) -> bool:
            nonlocal frequency_checker
            frequency_checker[word] -= 1
            return frequency_checker[word] >= 0

        def reduce_word_in_frequency_checker(word: str):
            nonlocal frequency_checker
            frequency_checker[word] -= 1

        def add_word_in_frequency_checker(word: str):
            nonlocal frequency_checker
            frequency_checker[word] += 1

        def check_word_frequency_checker() -> bool:
            return all(freq == 0 for freq in frequency_checker.values())

        # state
        output_indexes = set()

        for phase in range(min(m, n - w + 1)):
            logger.debug(f"  at phase={phase}, ...")
            prev_window_had_matched = False
            start = phase
            continue_prev_freq_checker = False
            while start < n - w + 1:
                qualifies = True
                orig_start = start
                logger.debug(
                    f"  at phase={phase}, start={orig_start}, candidate={s[start : start + w]}, prev_window_had_matched={prev_window_had_matched}, continue_prev_freq_checker={continue_prev_freq_checker}, frequency_checker={frequency_checker}"
                )
                if prev_window_had_matched:
                    new_word = s[start + w - m : start + w]
                    old_word = s[start - m : start]
                    if new_word != old_word:
                        if new_word not in word_frequency_map:
                            start += w
                            logger.debug(
                                f"  at phase={phase}, start={orig_start}, new_word={new_word} is not in frequency map, so restarting from start={start}"
                            )
                        else:
                            reduce_word_in_frequency_checker(new_word)
                            add_word_in_frequency_checker(old_word)
                            logger.debug(
                                f"  at phase={phase}, start={orig_start}, updated frequency_checker to {frequency_checker}"
                            )
                            qualifies = False
                            logger.debug(
                                f"  at phase={phase}, start={orig_start}, window is disqualified"
                            )
                else:
                    if continue_prev_freq_checker:
                        new_word = s[start + w - m : start + w]
                        old_word = s[start - m : start]
                        if new_word != old_word:
                            if new_word not in word_frequency_map:
                                start += w
                                logger.debug(
                                    f"  at phase={phase}, start={orig_start}, new_word={new_word} is not in frequency map, so restarting from start={start}"
                                )
                            else:
                                reduce_word_in_frequency_checker(new_word)
                                add_word_in_frequency_checker(old_word)
                                logger.debug(
                                    f"  at phase={phase}, start={orig_start}, updated frequency_checker to {frequency_checker}"
                                )
                        else:
                            logger.debug(
                                f"  at phase={phase}, start={orig_start}, window is just a repeat of the previous window, it is also disqualified"
                            )
                            qualifies = False
                    else:
                        reset_frequency_checker()  # frequency_checker <= frequency_map
                        logger.debug(
                            f"  at phase={phase}, start={orig_start}, initially, frequency_checker = {frequency_checker}"
                        )
                        for j in range(start, start + w, m):
                            word = s[j : j + m]
                            if word not in word_frequency_map:
                                # then abort this window, and check from the window starting at j+m
                                start = j + m
                                logger.debug(
                                    f"  at phase={phase}, start={orig_start}, word={word} is not in frequency map, so restarting from start={start}"
                                )
                                break
                            if qualifies:
                                if not check_word_in_frequency_checker(word):
                                    logger.debug(
                                        f"  at phase={phase}, start={orig_start}, at word={word}, word is not qualified in frequency_checker, so disqualified"
                                    )
                                    qualifies = False
                            else:
                                reduce_word_in_frequency_checker(word)
                            logger.debug(
                                f"  at phase={phase}, start={orig_start}, at word={word}, frequency_checker -> {frequency_checker}"
                            )
                    if (
                        start == orig_start
                        and qualifies
                        and not check_word_frequency_checker()
                    ):
                        qualifies = False
                        logger.debug(
                            f"  at phase={phase}, start={orig_start}, updated frequency_checker={frequency_checker} is not 0, so disqualified"
                        )
                if orig_start == start:
                    if qualifies:
                        prev_window_had_matched = True
                        output_indexes.add(start)
                    else:
                        prev_window_had_matched = False
                    start += m
                    continue_prev_freq_checker = True
                else:
                    continue_prev_freq_checker = False
                    prev_window_had_matched = False
        return list(output_indexes)


def Test(s: str, words: list[str], expected_output: list[int]) -> bool:
    output = Solution().findSubstring(s, words)

    def match(expected_output: list[int], output: list[int]) -> bool:
        return sorted(expected_output) == sorted(output)

    if not match(expected_output, output):
        if (
            len(s) <= 100
            and len(words) <= 100
            and len(output) < 100
            and len(expected_output) < 100
        ):
            logger.error(
                f"output(={output}) doesn't match expected_output(={expected_output}) for s={s}, words={words}"
            )
        else:
            logger.error("Failed. output doesn't match expected_output")
        return False
    else:
        if len(s) <= 100 and len(words) <= 100 and len(output) < 100:
            logger.info(f"Passed: output={output} for s={s}, words={words}")
        else:
            logger.info("Passed!")
    return False


Test("", ["", ""], [])
Test("abc", ["ab", "cd"], [])
Test("eabcdab", ["ab", "cd"], [3, 1])
Test("eabcdab", ["ab", "cd", "ab"], [1])
# Test("eaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"], [i for i in range(1, 135)])
Test("eaaaaaaaaaaa", ["a", "a", "a", "a"], list(range(1, 9)))
Test("abcd", ["abc"], [0])
Test("eabcd", ["abc"], [1])
Test("".join(["a"] * 10000), ["a"], list(range(10000)))
Test("e" + "".join(["a"] * 9999), ["a"], list(range(1, 10000)))
Test(
    "ababbaabababbababaababa",
    ["a", "b", "a", "b"],
    [0, 2, 3, 4, 6, 7, 8, 10, 12, 13, 14, 16, 18, 19],
)
Test("".join(["a"] * 100000), ["a"], list(range(100000)))
Test("".join(["a"] * 10000), ["a"] * 5000, list(range(5001)))
Test("".join(["ab"] * 10000), ["ab"] * 5000, list(range(0, 10002, 2)))
Test("".join(["a"] * 10000), ["a"] * 5000, list(range(5001)))
Test("barfoofoobarthefoobarman", ["bar", "foo", "the"], [6, 9, 12])
Test(
    "bcabbcaabbccacacbabccacaababcbb",
    ["c", "b", "a", "c", "a", "a", "a", "b", "c"],
    [6, 16, 17, 18, 19, 20],
)
Test("mississippi", ["is"], [1, 4])
