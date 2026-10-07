from collections import Counter


def minimum_window(s: str, t: str) -> str:
    """
    Args:
     s(str)
     t(str)
    Returns:
     str
    """
    # Write your code here.
    n = len(s)
    l = len(t)
    assert 1 <= n <= 10**5
    assert 1 <= l <= 10**5
    if n < l:
        return ""
    # freq_s = Counter(s)
    freq_t = Counter(t)
    # print(f"n={n}, l={l}, freq_t={freq_t}")

    def freq_delta(freq1: dict[str, int], freq2: dict[str, int]) -> dict[str, int]:
        delta = freq1.copy()
        for c, count in freq2.items():
            if count == 0:  # needed ?
                continue
            if c not in delta:
                delta[c] = -count
            else:
                delta[c] -= count
                if delta[c] == 0:
                    del delta[c]
        return delta

    def freq_has_any_negatives(freq: dict[str, int]) -> bool:
        return any(val < 0 for val in freq.values())

    def update_freq(freq: dict[str, int], outgoing_char: str, incoming_char: str):
        if outgoing_char == incoming_char:
            return
        if outgoing_char in freq:
            freq[outgoing_char] -= 1
            if freq[outgoing_char] == 0:
                del freq[outgoing_char]
        else:
            freq[outgoing_char] = -1
        if incoming_char in freq:
            freq[incoming_char] += 1
        else:
            freq[incoming_char] = 1

    def find_valid_substring_of_length(k: int) -> str | None:
        # print(f"find_valid_substring_of_length({k})")
        assert n >= k >= l
        window = s[:k]
        freq_window = Counter(window)
        delta = freq_delta(freq_window, freq_t)
        # print(f"  first window={window}, freq_window={freq_window}, delta={delta}")
        if not freq_has_any_negatives(delta):
            # print(f"    window={window} of length {k} matched. Returned")
            return window
        for i in range(k, n):
            update_freq(delta, s[i - k], s[i])
            # print(
            #     f"  window with i={i}: window={s[i - k + 1 : i + 1]}, updated delta={delta}"
            # )
            if not freq_has_any_negatives(delta):
                # print(
                #     f"    window={s[i - k + 1 : i + 1]} of length={k} matched. Returned"
                # )
                return s[i - k + 1 : i + 1]
        return None

    start, end = l, n
    best_str, best_str_len = None, n + 1
    while start <= end:
        mid = (start + end) // 2
        found_substr = find_valid_substring_of_length(mid)
        if found_substr is not None:
            if len(found_substr) < best_str_len:
                best_str = found_substr
                best_str_len = len(s)
                # print(f"best_str={best_str}, best_str_len={best_str_len}")
            end = mid - 1
        else:
            start = mid + 1

    return "" if best_str_len > n else best_str


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, t: str, expected: int) -> tuple[bool, str]:
    actual = minimum_window(s, t)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="AYZABOBECODXBANC", t="ABC", expected="BANC")
            Test(s="BACRDESDFBAER", t="BAR", expected="BACR")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
