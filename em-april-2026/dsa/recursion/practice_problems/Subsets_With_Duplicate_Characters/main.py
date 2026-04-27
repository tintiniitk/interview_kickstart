import sys

"""

Subsets With Duplicate Characters
Given a string that might contain duplicate characters, find all the possible distinct subsets of that string.

Example One
{
"s": "aab"
}
Output:

["", "a", "aa", "aab", "ab", "b"]
Example Two
{
"s": "dc"
}
Output:

["", "c", "cd", "d"]
Notes
All the subset strings should be individually sorted.
The order of the output strings does not matter.
Constraints:

1 <= length of the string <= 15
String consists of lowercase English letters

"""


def helper(
    freq: dict[str, int],
    unique_chars: list[str],
    slate: list[str],
    done: int,
    filled: int,
    ret: list[str],
):
    if done == len(slate):
        ret.append("".join(slate[:filled]))
        return
    next_char = unique_chars[0]
    next_char_freq = freq[next_char]
    for i in range(0, next_char_freq + 1):
        slate[filled : filled + i] = [next_char] * i
        helper(freq, unique_chars[1:], slate, done + next_char_freq, filled + i, ret)


def get_distinct_subsets(s: str) -> list[str]:
    """
    Args:
     s(str)
    Returns:
     list_str
    """
    # Write your code here.
    freq = {}
    for c in s:
        if c in freq:
            freq[c] = freq[c] + 1
        else:
            freq[c] = 1
    unique_chars = list(freq.keys())
    ret = []
    helper(freq, unique_chars, ["."] * len(s), 0, 0, ret)
    return ret


if __name__ == "__main__":
    s = "aab"
    expected_output = None
    if len(sys.argv) > 1:
        s = sys.argv[1]
    else:
        expected_output = ["", "a", "aa", "aab", "ab", "b"]
    actual_output = get_distinct_subsets(s)
    print(f"s={s}, expected_output={expected_output}, actual_output={actual_output}")
    pass
