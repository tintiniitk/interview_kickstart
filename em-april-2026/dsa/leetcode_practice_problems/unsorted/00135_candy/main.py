from typing import List
from itertools import pairwise
from collections import defaultdict, deque


class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)

        # adj = defaultdict(set)
        # in_degrees = [0] * n
        # for i, j in pairwise(range(n)):
        #     if ratings[i] > ratings[j]:
        #         adj[j].add(i)
        #         in_degrees[i] += 1
        #     elif ratings[i] < ratings[j]:
        #         adj[i].add(j)
        #         in_degrees[j] += 1
        # candies = [0] * n
        # # # DFS based recursive approach
        # # def traverse(i: int, v: int):
        # #     if candies[i] < v:
        # #         candies[i] = v
        # #         for nxt_nbr in adj[i]:
        # #             traverse(nxt_nbr, v + 1)
        # # for i in range(n):
        # #     if in_degrees[i] == 0:
        # #         traverse(i, 1)
        # # BFS approach
        # q = deque([(i, 1) for i in range(n) if in_degrees[i] == 0])
        # while q:
        #     i, v = q.popleft()
        #     if candies[i] < v:
        #         candies[i] = v
        #         for nbr in adj[i]:
        #             q.append((nbr, v + 1))

        candies = [1] * n
        for i, j in pairwise(range(n)):
            if ratings[j] > ratings[i]:
                candies[j] = max(candies[j], candies[i] + 1)
        for i, j in pairwise(range(n - 1, -1, -1)):
            if ratings[j] > ratings[i]:
                candies[j] = max(candies[j], candies[i] + 1)

        return sum(candies)


from utils.pretty_test_runner import pretty_test_runner, truncate_param
from utils.context_manager import time_limit, TimeoutException


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(ratings: List[int], expected: int) -> (bool, str):
    actual = Solution().candy(ratings)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print(f"Running tests ...")
        with time_limit(5):
            Test(ratings=[1, 0, 2], expected=5)
            Test(ratings=[1, 2, 2], expected=4)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
    except Exception as e:
        print(f"Tests failed: {e}")
        raise e


if __name__ == "__main__":
    main()
