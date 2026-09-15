class Solution:
    def hIndex(self, citations: list[int]) -> int:
        count = 0
        max_h_index = 0
        n = len(citations)
        for i in range(n - 1, -1, -1):
            num_citations = citations[i]
            if num_citations == 0:
                break
            count = n - i
            if count >= num_citations > max_h_index:
                return num_citations
            if count <= num_citations:
                max_h_index = max(max_h_index, count)
        return max_h_index


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
            Test(citations=[0, 1, 3, 5, 6], expected=3)
            Test(citations=[1, 2, 100], expected=2)
            Test(citations=[100], expected=1)
            Test(citations=[0, 0, 4, 4], expected=2)
            Test(citations=[1, 4, 7, 9], expected=3)

    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
