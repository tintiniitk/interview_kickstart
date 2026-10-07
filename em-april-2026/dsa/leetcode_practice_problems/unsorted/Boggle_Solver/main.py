from collections import Counter


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None


def boggle_solver(dictionary: list[str], mat: list[str]) -> list[str]:
    """
    Args:
     dictionary(list_str)
     mat(list_str)
    Returns:
     list_str
    """
    if not dictionary or not mat or not mat[0]:
        return []

    n = len(mat)
    m = len(mat[0])

    is_mat_homogeneus = False
    first_value = mat[0][0]
    is_mat_homogeneus = all(value == first_value for row in mat for value in row)
    if is_mat_homogeneus:
        num_values = n * m
        dictionary = list(
            set(dictionary)
        )  # remove duplicates from dictionary as the question allows them, for some weird reason.
        found_words = []
        for word in dictionary:
            freq = Counter(word)
            if (
                first_value in freq
                and freq[first_value] == len(word)
                and len(word) <= num_values
            ):
                found_words.append(word)
        return sorted(found_words)

    # Step 1: Build the Trie from the dictionary
    root = TrieNode()
    for word in dictionary:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.word = word

    found_words = set()

    # 8 possible directions (horizontal, vertical, diagonal)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    visited = [[False] * m for _ in range(n)]

    def dfs(r, c, node):
        char = mat[r][c]
        if char not in node.children:
            return

        next_node = node.children[char]

        # If we found a valid dictionary word, add it to our set
        if next_node.is_end and next_node.word:
            found_words.add(next_node.word)

        visited[r][c] = True

        # Explore all 8 adjacent neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc]:
                dfs(nr, nc, next_node)

        # Backtrack
        visited[r][c] = False

    # Step 2: Start DFS from every cell in the matrix
    for i in range(n):
        for j in range(m):
            if mat[i][j] in root.children:
                dfs(i, j, root)

    return list(found_words)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=5, stop_on_tc_failure=False)
def Test(
    dictionary: list[str], mat: list[str], expected: list[str]
) -> tuple[bool, str]:
    actual = boggle_solver(dictionary, mat)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                dictionary=["bst", "heap", "tree"],
                mat=["bsh", "tee", "arh"],
                expected=["bst", "tree"],
            )
            Test(
                dictionary=["abs", "tabs", "hell", "bst", "hello"],
                mat=["adfresd", "nbshell", "ottoooo", "bhjkdfr", "dfcsfdf", "bstfdfs"],
                expected=["abs", "bst", "hell", "hello"],
            )
            Test(
                dictionary=["bst", "help", "ab", "b", "d"],
                mat=["abc", "def"],
                expected=["ab", "b", "d"],
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
