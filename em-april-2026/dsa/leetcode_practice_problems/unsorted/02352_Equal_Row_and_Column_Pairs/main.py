from collections import defaultdict
from typing import List
from collections import Counter


class Solution:
    # my solution
    def equalPairs(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 1:
            return 1
        row_hash_counts = Counter(tuple(row) for row in grid)
        num_matches = 0
        for j in range(n):
            col = [grid[i][j] for i in range(n)]
            num_matches += row_hash_counts[tuple(col)]
        return num_matches


def Test(grid: List[List[int]], expected_count: int) -> bool:
    actual_count = Solution().equalPairs(grid)
    assert (
        actual_count == expected_count
    ), f"actual_count={actual_count} didn't match expected_count={expected_count} for input grid={grid}"
    return True


Test([[3, 2, 1], [1, 7, 6], [2, 7, 7]], 1)
Test([[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]], 3)
Test([[1] * 200] * 200, 40000)  # worst-case
