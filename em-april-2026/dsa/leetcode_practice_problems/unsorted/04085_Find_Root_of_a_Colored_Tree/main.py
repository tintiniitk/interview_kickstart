from collections import deque


class Solution:
    def findColoredRoot(self, edges: list[list[int]], colors: str) -> int:
        n = len(edges) + 1

        def find_root_candidates_and_children() -> tuple[list[int], list[set]]:
            # assert n >= 2
            # assert len(colors) == n
            children_of = [set() for _ in range(n)]
            parent_of = [-1] * n
            parent_to_child_color_mapping = {"R": "B", "B": "W", "W": "R"}
            is_candidate_for_root = [True] * n
            for n1, n2 in edges:
                n1_color = colors[n1]
                n2_color = colors[n2]
                if n2_color == parent_to_child_color_mapping[n1_color]:
                    children_of[n1].add(n2)
                    if 0 <= parent_of[n2] < n and parent_of[n2] != n1:
                        return [], []
                    parent_of[n2] = n1
                    n1_out_degree = len(children_of[n1])
                    is_candidate_for_root[n1] &= n1_out_degree <= 2
                    is_candidate_for_root[n2] = False
                else:
                    is_candidate_for_root[n1] = False
                    if n1_color == parent_to_child_color_mapping[n2_color]:
                        children_of[n2].add(n1)
                        if 0 <= parent_of[n1] < n and parent_of[n1] != n2:
                            return [], []
                        parent_of[n1] = n2
                        n2_out_degree = len(children_of[n2])
                        is_candidate_for_root[n2] &= n2_out_degree <= 2
                    else:
                        is_candidate_for_root[n2] = False
            return [
                i for i in range(n) if is_candidate_for_root[i] and children_of[i]
            ], children_of

        candidates, children = find_root_candidates_and_children()
        if not candidates:
            return -1
        # print(f"candidates={candidates}")
        print(f"num-candidates={len(candidates)}")
        # print(f"is 33333 in candidates={33333 in candidates}")
        for candidate in candidates:
            # print(f"trying candidate={candidate}")
            visited = [False] * n
            q = deque([candidate])
            num_visited = 1
            visited[candidate] = True
            is_valid = True
            while q and is_valid:
                num_in_q = len(q)
                # print(f" level: q={q}")
                for _ in range(num_in_q):
                    node = q.popleft()
                    for nbr in children[node]:
                        if visited[nbr]:
                            is_valid = False
                            break
                        q.append(nbr)
                        visited[nbr] = True
                        num_visited += 1
                    if not is_valid:
                        break
            if is_valid and num_visited == n:
                return candidate
        return -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=4.9, stop_on_tc_failure=False)
def Test(edges: list[list[int]], colors: str, expected: int) -> tuple[bool, str]:
    actual = Solution().findColoredRoot(edges, colors)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            # Test(edges=[[3, 1], [3, 2], [1, 4], [2, 0]], colors="BRRWB", expected=3)
            # Test([[0, 1], [1, 2], [2, 3]], colors="RBRB", expected=-1)
            # Test(edges=[[1, 0], [0, 2], [3, 0]], colors="WBRR", expected=1)
            Test(**tc_x_tc)
            # Test(edges=    , colors =  , expected=   )
            # Test(edges=    , colors =  , expected=   )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
