from collections import defaultdict
from heapq import heappop, heappush


class Solution:
    def findLadders(
        self, beginWord: str, endWord: str, wordList: list[str]
    ) -> list[list[str]]:
        if beginWord == endWord:
            return [[beginWord, endWord]]
        words = set(wordList)

        # helper
        def dist(word1: str, word2: str) -> int:
            return sum(c1 != c2 for c1, c2 in zip(word1, word2))

        # assume endWord and all words in words are also of length k
        adj_lists = defaultdict(set)
        for i, word in enumerate(wordList):
            for j in range(i + 1, len(words)):
                word2 = wordList[j]
                if dist(word, word2) == 1:  # word != word2 and
                    adj_lists[word].add(word2)
                    adj_lists[word2].add(word)
        if beginWord not in words:
            for word2 in wordList:
                if dist(beginWord, word2) == 1:  # beginWord != word2 and
                    adj_lists[beginWord].add(word2)
                    adj_lists[word2].add(beginWord)
        # print(f"adj_lists={adj_lists}")

        # find min_dist to endWord from each word, including from beginWord
        distances: dict[str, int] = {word: len(words) + 1 for word in words}
        distances[endWord] = 0
        pq = [(0, endWord)]
        min_distance_bw_begin_end = len(words) + 1
        min_distance_prev_node = defaultdict(None)
        min_distance_prev_node[endWord] = None
        while pq:
            distance, word = heappop(pq)
            if word == beginWord:
                if distance < min_distance_bw_begin_end:
                    min_distance_bw_begin_end = distance
                    distances[beginWord] = distance
                continue
            if word in adj_lists:
                for nxt in adj_lists[word]:
                    if nxt not in distances or distance + 1 < distances[nxt]:
                        min_distance_prev_node[nxt] = word
                        distances[nxt] = distance + 1
                        heappush(pq, (distance + 1, nxt))
        # print(f"min_distance_bw_begin_end = {min_distance_bw_begin_end}")
        # print(f"min_distance_prev_node = {min_distance_prev_node}")
        # print(f"distances = {distances}")
        rev_dist_map: list[list[str]] = (
            [[endWord]]
            + [[] for _ in range(min_distance_bw_begin_end - 1)]
            + [[beginWord]]
        )
        # print(f"rev_dist_map = {rev_dist_map}")
        for word, distance in distances.items():
            if 0 < distance < min_distance_bw_begin_end:
                rev_dist_map[distance].append(word)
        # print(f"rev_dist_map = {rev_dist_map}")

        distance = min_distance_bw_begin_end
        slate = [beginWord]
        ret = []

        def process(distance: int, word: str):  # , level: int
            # print(f"{'  ' * level}process({distance}, {slate})")
            if distance == 0:
                ret.append(slate.copy())
                return
            if distance == 1:
                slate.append(endWord)
                process(0, endWord)  # , level + 1
                slate.pop()
                return
            for nxt in rev_dist_map[distance - 1]:
                if nxt in adj_lists[word]:
                    slate.append(nxt)
                    process(distance - 1, nxt)  # , level + 1
                    slate.pop()

        slate = [beginWord]
        ret = []
        process(min_distance_bw_begin_end, beginWord)  # , 0
        # print(f"ret = {ret}")
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import eq_list_int, pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.1, stop_on_tc_failure=False)
def Test(
    beginWord: str, endWord: str, wordList: list[str], expected: list[list[str]]
) -> tuple[bool, str]:
    actual = Solution().findLadders(beginWord, endWord, wordList)
    # passed, errmsg = eq_list_int(actual, expected)
    # if not passed:
    #     return False, errmsg
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                beginWord="hit",
                endWord="cog",
                wordList=["hot", "dot", "dog", "lot", "log", "cog"],
                expected=[
                    ["hit", "hot", "dot", "dog", "cog"],
                    ["hit", "hot", "lot", "log", "cog"],
                ],
            )
            Test(
                beginWord="hit",
                endWord="cog",
                wordList=["hot", "dot", "dog", "lot", "log"],
                expected=[],
            )
            Test(
                beginWord="abc",
                endWord="cde",
                wordList=[
                    "abc",
                    "cbc",
                    "abe",
                    "adc",
                    "ebe",
                    "edc",
                    "cdc",
                    "ebc",
                    "cde",
                ],
                expected=[["abc", "cbc", "cdc", "cde"], ["abc", "adc", "cdc", "cde"]],
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
