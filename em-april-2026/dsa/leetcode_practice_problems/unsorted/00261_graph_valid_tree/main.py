# https://leetcode.com/problems/graph-valid-tree

from collections import deque


class Solution:
    def validTree(self, n: int, edges: list[list[int]]) -> bool:
        adj_lists = [[] for _ in range(n)]
        # num_unique_edges = 0
        for edge in edges:
            head = edge[0]
            tail = edge[1]
            # input validation
            if head == tail or head < 0 or head >= n or tail < 0 or tail >= n:
                print(f"Input edge {head} -> {tail} is not valid")
                return False
            # if not tail in adj_lists[head] and not head in adj_lists[tail]:
            #     num_unique_edges = num_unique_edges + 1
            adj_lists[head].append(tail)
            adj_lists[tail].append(head)

        # if num_unique_edges != (n - 1):
        #     print(
        #         f"Too many edges found for valid tree. Got = {num_unique_edges}, Expected: {n-1}"
        #     )
        #     return False

        print(f"edges = {edges}, adj_lists = {adj_lists}")

        visited = [0 for _ in range(n)]

        parent_of = [-1 for _ in range(n)]
        level = 0

        def dfs(node: int) -> bool:  # Return True if there a cycle
            nonlocal parent_of
            nonlocal level
            # print(f"{'.'*level}dfs({node}) with parent_of={parent_of}, visited={visited}")
            visited[node] = 1
            for nbr in adj_lists[node]:
                # print(
                # f"{'.'*level}Going to visit neighbor {nbr} with parent_of={parent_of}, visited={visited}"
                # )
                if visited[nbr] == 0:
                    parent_of[nbr] = node
                    level = level + 1
                    if dfs(nbr):
                        level = level - 1
                        return True
                    level = level - 1
                elif nbr != parent_of[node]:
                    print(
                        f"{'.'*level}node {nbr} is visited twice, once from {node} and once from somewhere else, caught in the neighbor {nbr} of {node}"
                    )
                    return True

        def bfs(node: int) -> bool:  # Return True if there a cycle
            nonlocal parent_of
            visited[node] = 1
            q = deque([node])
            while len(q) > 0:
                parent = q.popleft()
                for nbr in adj_lists[parent]:
                    if visited[nbr] == 0:
                        parent_of[nbr] = parent
                        visited[nbr] = 1
                        q.append(nbr)
                    elif nbr != parent_of[parent]:
                        print(
                            f"node {parent} is visited twice, once from {parent_of[parent]} and once from {nbr}, caught in the neighbor {nbr} of {parent}"
                        )
                        return True

        numConnectedComponents = 0
        for unvisited in range(n):
            if visited[unvisited] == 0:
                if numConnectedComponents > 0:
                    print(
                        f"Found a second connected-component started at node {unvisited}"
                    )
                    return False

                # print(f"Starting a new DFS from {unvisited}, with visited={visited}")
                numConnectedComponents = numConnectedComponents + 1
                # if dfs(unvisited):
                if bfs(unvisited):
                    return False
                # print(f"Finished DFS started from {unvisited}, with visited={visited}")

        return True


if __name__ == "__main__":
    n = 6
    # edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
    edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 3]]
    s = Solution()
    valid = s.validTree(n, edges)
    print(f"n={n}, edges={edges}, is_valid={valid}")
