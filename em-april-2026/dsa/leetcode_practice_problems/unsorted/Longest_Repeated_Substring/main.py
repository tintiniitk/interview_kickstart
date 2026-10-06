def get_longest_repeated_substring(s: str) -> str:
    """
    Args:
     s(str)
    Returns:
     str
    """
    # Write your code here.
    """
    Finds the longest repeating substring using Binary Search + Rolling Hash (Rabin-Karp).

    Time Complexity: O(N log N) average
    Space Complexity: O(N)
    """
    n = len(s)
    if n < 2:
        return ""

    # Convert characters to 1-based integer values (a=1, b=2, ..., z=26)
    nums = [ord(c) - ord("a") + 1 for c in s]

    # Large prime modulus and base for double hashing to avoid collisions
    MOD = 2**63 - 1  # Mersenne prime for fast double hashing/large bounds
    BASE = 31

    def search_length(length: int) -> int:
        """
        Checks if there exists any repeating substring of the given 'length'.
        Returns the starting index of the first occurrence if found, else -1.
        """
        if length == 0:
            return -1

        # Compute BASE^(length - 1) % MOD
        base_pow = pow(BASE, length - 1, MOD)

        # Compute hash for the first window of size 'length'
        current_hash = 0
        for i in range(length):
            current_hash = (current_hash * BASE + nums[i]) % MOD

        seen_hashes = {current_hash: 0}

        for start in range(1, n - length + 1):
            # Roll the hash window: remove left char, add right char
            prev_char = nums[start - 1]
            new_char = nums[start + length - 1]

            current_hash = (current_hash - prev_char * base_pow) % MOD
            current_hash = (current_hash * BASE + new_char) % MOD

            if current_hash in seen_hashes:
                prev_start = seen_hashes[current_hash]
                # Secondary verification step to eliminate hash collisions completely
                if s[prev_start : prev_start + length] == s[start : start + length]:
                    return start
            else:
                seen_hashes[current_hash] = start

        return -1

    # Binary search for the maximum possible length L in range [1, N - 1]
    low, high = 1, n - 1
    best_start = -1
    best_len = 0

    while low <= high:
        mid = (low + high) // 2
        start_idx = search_length(mid)
        if start_idx != -1:
            best_start = start_idx
            best_len = mid
            low = mid + 1  # Try searching for a longer valid substring
        else:
            high = mid - 1  # Try a shorter length

    return s[best_start : best_start + best_len] if best_start != -1 else ""


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: int) -> tuple[bool, str]:
    actual = get_longest_repeated_substring(s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="efabcdhefhabcdiefi", expected="abcd")
            Test(s="aaaaa", expected="aaaa")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
