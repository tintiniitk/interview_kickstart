from typing import List
from collections import deque


class Solution:
    def remainingMethods(
        self, n: int, k: int, invocations: List[List[int]]
    ) -> List[int]:
        dependency_methods = {}  # int -> set
        in_degress = [0 for _ in range(n)]
        out_degress = [0 for _ in range(n)]
        for invocation in invocations:
            dependent, dependency = invocation[0], invocation[1]
            if dependent not in dependency_methods:
                dependency_methods[dependent] = set([dependency])
            else:
                dependency_methods[dependent].add(dependency)
            in_degress[dependency] += 1
            out_degress[dependent] += 1
        suspicious_methods = set([k])

        # # expensive bfs with cyclicity-check
        # level = 0
        # q = deque([k])
        # num_q = len(q)
        # while num_q > 0:
        #     if level >= n:
        #         raise ValueError(f"Found cycles in the dependency-graph")
        #     i = 0
        #     level += 1
        #     for i in range(num_q):
        #         bugged_dependent = q.popleft()
        #         if bugged_dependent in dependency_methods:
        #             for dependency_method in dependency_methods[bugged_dependent]:
        #                 if dependency_method not in suspicious_methods:
        #                     q.append(dependency_method)
        #                     suspicious_methods.add(dependency_method)
        #     num_q = len(q)

        # # inexpensive bfs without cyclicity-check
        q = deque([k])
        while q:
            bugged_dependent = q.popleft()
            if bugged_dependent in dependency_methods:
                for dependency_method in dependency_methods[bugged_dependent]:
                    if dependency_method not in suspicious_methods:
                        q.append(dependency_method)
                        suspicious_methods.add(dependency_method)

        full_set = set(range(n))
        remaining_methods = full_set - suspicious_methods

        # # initially developed O(V+E) complexity approach for verification.
        # for remaining_method in remaining_methods:
        #     if remaining_method in dependency_methods:
        #         for dependency_method in dependency_methods[remaining_method]:
        #             if dependency_method in suspicious_methods:
        #                 return list(full_set)

        if sum([in_degress[i] for i in suspicious_methods]) != sum(
            [out_degress[i] for i in suspicious_methods]
        ):
            return list(full_set)

        return list(remaining_methods)


def Test(n: int, k: int, invocations: List[List[int]], expected: List[int]):
    print(f"[RUN]\n  n={n}, k={k}, invocations={invocations}")
    actual = Solution().remainingMethods(n, k, invocations)
    assert sorted(actual) == sorted(
        expected
    ), f"actual={actual}, expected={expected}, for n={n}, k={k}, invocations={invocations}\n[FAILED]"
    print("[DONE]")


Test(4, 1, [[1, 2], [0, 1], [3, 2]], [0, 1, 2, 3])
Test(5, 0, [[1, 2], [0, 2], [0, 1], [3, 4]], [3, 4])
Test(3, 2, [[1, 2], [0, 1], [2, 0]], [])
