from collections import Counter


class Solution:
    def hIndex(self, citations: list[int]) -> int:
        # # counter = Counter(citations)
        # num_citations_freq = [0] * 1001
        # for num_citations in citations:
        #     num_citations_freq[num_citations] += 1
        counter = Counter(citations)
        num_citations_freq = [
            counter.get(num_citations, 0) for num_citations in range(1001)
        ]
        if num_citations_freq[1000] >= 1000:
            return 1000
        for i in range(999, 0, -1):
            num_citations_freq[i] += num_citations_freq[i + 1]
            if num_citations_freq[i] >= i:
                return i
        return 0


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(citations: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().hIndex(citations)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(citations=[3, 0, 6, 1, 5], expected=3)
            Test(citations=[1, 3, 1], expected=1)
            Test(citations=[0, 0, 0, 0, 0], expected=0)
            Test(citations=[5, 6, 7, 8, 9], expected=5)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
