# https://leetcode.com/problems/count-the-number-of-complete-components

"""

You are given an integer n. There is an undirected graph with n vertices, numbered from 0 to n - 1. You are given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting vertices ai and bi.

Return the number of complete connected components of the graph.

A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.

A connected component is said to be complete if there exists an edge between every pair of its vertices.

Example 1:

Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]
Output: 3
Explanation: From the picture above, one can see that all of the components of this graph are complete.
Example 2:

Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]
Output: 1
Explanation: The component containing vertices 0, 1, and 2 is complete since there is an edge between every pair of two vertices.
On the other hand, the component containing vertices 3, 4, and 5 is not complete since there is no edge between vertices 4 and 5. Thus, the number of complete components in this graph is 1.


Constraints:

1 <= n <= 50
0 <= edges.length <= n * (n - 1) / 2
edges[i].length == 2
0 <= ai, bi <= n - 1
ai != bi
There are no repeated edges.

"""


class Solution:
    def countCompleteComponents(self, n: int, edges: list[list[int]]) -> int:
        adj_lists = [[] for _ in range(n)]
        for edge in edges:
            head = edge[0]
            tail = edge[1]
            adj_lists[head].append(tail)
            adj_lists[tail].append(head)

        all_visited_nodes_so_far = set()
        current_connected_component = []

        def dfs(node: int):
            nonlocal all_visited_nodes_so_far
            nonlocal current_connected_component
            if node not in all_visited_nodes_so_far:
                all_visited_nodes_so_far.add(node)
                current_connected_component.append(node)
                for nbr in adj_lists[node]:
                    dfs(nbr)

        # numConnectedComponents = 0
        numCompleteConnectedComponents = 0

        for next_unvisited_node in range(n):
            if not next_unvisited_node in all_visited_nodes_so_far:
                # numConnectedComponents = numConnectedComponents + 1

                # #debug
                # print(f"Found next_unvisited_node node: {next_unvisited_node}. numConnectedComponents updated to {numConnectedComponents}. Before visting it, all_visited_nodes_so_far={all_visited_nodes_so_far}")

                current_connected_component = []
                dfs(next_unvisited_node)
                num_connected = len(current_connected_component)
                is_complete = all(
                    len(adj_lists[node]) == (num_connected - 1)
                    for node in current_connected_component
                )
                if is_complete:
                    numCompleteConnectedComponents = numCompleteConnectedComponents + 1

                # #debug
                # print(f"Finished visiting node: {next_unvisited_node}. After visting it, all_visited_nodes_so_far={all_visited_nodes_so_far}, numCompleteConnectedComponents updated to {numCompleteConnectedComponents}")

        return numCompleteConnectedComponents


if __name__ == "__main__":
    n = 6
    edges = [[0, 1], [0, 2], [1, 2], [3, 4]]
    res = Solution().countCompleteComponents(n, edges)
    print(f"n = {n}, edges = {edges}, countCompleteComponents = {res}")
