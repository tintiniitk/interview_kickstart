import sys
from collections import deque


# @profile
def dist(word1: str, word2: str) -> int:
    # """Assumes that word1 and word2 are same length"""
    # if not word1 and not word2:
    #     return 0
    # if not word1 or not word2:
    #     raise ValueError(f": dist({word1}, {word2}). One of the inputs is null.")
    # n = len(word1)
    # if n != len(word2):
    #     raise ValueError(f": dist({word1}, {word2}). Inputs have different lengths.")
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))


# @profile
def string_transformation(words, start, stop):
    """
    Args:
     words(list_str)
     start(str)
     stop(str)
    Returns:
     list_str
    """
    # Write your code here.
    if not start or not stop:
        raise ValueError(f"At least one out of start and stop is null")
    n = len(start)
    if n != len(stop):
        raise ValueError(f"start={start} and stop={stop} have different lengths.")
    if start == stop and (not words or len(words) == 0):
        return ["-1"]
    if dist(start, stop) == 1:
        return [start, stop]
    words_set = set(words)
    visited = set()
    min_path_length = len(words_set) + 3
    min_length_path = []
    alphabet = list("abcdefghijklmnopqrstuvwxy")
    q = deque([([start], -1)])
    min_distance_path_from = {word: None for word in words_set}
    min_distance_path_from[stop] = []
    min_distance_path_from[start] = None

    while len(q) > 0:
        path, lastCharIndexChanged = q.popleft()
        word = path[-1]
        path_length = len(path)
        # print(f"path={path}, dist_to_go={dist_to_go}, min_length_path={min_length_path})")
        if word == stop:
            if path_length == 1:
                # path is too short, ignoring this.
                # print(f" path {path} is too short, ignoring this")
                pass
            else:
                for i in range(path_length - 1):
                    w = path[i]
                    new_min_distance_path_from_w = path[i + 1 :]
                    if not min_distance_path_from[w] or len(
                        min_distance_path_from[w]
                    ) > len(new_min_distance_path_from_w):
                        min_distance_path_from[w] = new_min_distance_path_from_w
                if path_length < min_path_length:
                    min_length_path = path
                    min_path_length = path_length
                    # print(f" ----------- Updated min-path to {min_length_path}")
                continue

        # DP - desperate attempt to cut off branches.
        if min_distance_path_from[word]:
            if path_length + len(min_distance_path_from[word]) < min_path_length:
                min_length_path = path + min_distance_path_from[word]
                min_path_length = len(min_length_path)
            continue

        dist_to_go = dist(word, stop)
        if path_length + dist_to_go > min_path_length - 1:
            # this has already taken too many steps to improve on the existing best, terminate!
            # print(
            #     f"terminating path {path} because it won't improve on existing min-path"
            # )
            continue
        if dist_to_go == 1:
            q.append((path + [stop], -1))
            continue

        # if tuple(path) in visited:
        #     # going in circles, abandon!
        #     # print(f"Abandoning path {path} because it is already marked visited")
        #     continue
        # visited.add(tuple(path))
        new_word = list(word)
        for i in range(n):
            if i == lastCharIndexChanged:
                continue
            c = word[i]
            for new_char in alphabet:
                # print(f"new_char={new_char}")
                if not new_char == c:
                    new_word[i] = new_char
                    new_word_str = "".join(new_word)
                    # print(f"new_word_str={new_word_str}")
                    if new_word_str not in words_set:
                        # print(f"{new_word_str} not in words_set")
                        continue
                    q.append((path + [new_word_str], i))
            new_word[i] = c

    if min_path_length > len(words_set) + 2:
        return ["-1"]
    return min_length_path


if __name__ == "__main__":
    start = "bat"
    stop = "had"
    words = ["cat", "hat", "bad", "had"]
    if len(sys.argv) > 2:
        start = sys.argv[1]
        stop = sys.argv[2]
        words = sys.argv[3:]
    path = string_transformation(words, start, stop)
    if len(words) < 500:
        print(f"start={start}, stop={stop}, words={words}, path={path}")
    else:
        print(f"start={start}, stop={stop}, path={path}")
