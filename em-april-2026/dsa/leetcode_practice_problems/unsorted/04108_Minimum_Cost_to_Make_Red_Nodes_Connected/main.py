from collections import deque
from dataclasses import dataclass

INF_COST: int = 10**12


@dataclass
class TreeNode:
    val: int
    level: int  # 0 for root
    children: list["TreeNode"]
    color: str
    weight: int = 0
    cost_to_blackify: int = INF_COST
    min_cost_to_connect_reds_unconditional: int = INF_COST
    min_cost_to_connect_reds_with_red_at_root: int = INF_COST


class Solution:
    def minCost(self, n: int, colors: str, edges: list[list[int]]) -> int:
        adjLists = [set() for _ in range(n)]
        for u, v in edges:
            adjLists[u].add(v)
            adjLists[v].add(u)
        root = TreeNode(val=0, level=0, children=[], color=colors[0])
        visited = [False] * n
        visited[0] = True
        q = deque([root])
        while q:
            node = q.popleft()
            for child in adjLists[node.val]:
                if not visited[child]:
                    childNode = TreeNode(
                        val=child,
                        level=node.level + 1,
                        children=[],
                        color=colors[child],
                    )
                    visited[child] = True
                    q.append(childNode)
                    node.children.append(childNode)

        def assign_weight(node: TreeNode) -> int:
            if not node:
                return 0
            if not node.children:
                node.weight = 1
                return 1
            node.weight = 1 + sum(
                assign_weight(childNode) for childNode in node.children
            )
            return node.weight

        assign_weight(root)

        def post_order_traversal(node: TreeNode):
            if not node:
                return 0
            for childNode in node.children:
                post_order_traversal(childNode)

            node.cost_to_blackify = node.weight if node.color == "R" else 0
            node.min_cost_to_connect_reds_with_red_at_root = 0
            cost_to_blackify_children = sum(
                childNode.cost_to_blackify for childNode in node.children
            )
            if (
                cost_to_blackify_children > 0
            ):  # there is at least one red child somewhere in the sub-tree.
                node.cost_to_blackify += cost_to_blackify_children

                has_children_with_reds = False
                node.min_cost_to_connect_reds_with_red_at_root = 0
                for childNode in node.children:
                    if childNode.cost_to_blackify == 0:
                        continue
                    if node.min_cost_to_connect_reds_with_red_at_root == 0:
                        has_children_with_reds = True
                        continue
                    # find which is less costly, blackification or
                    if (
                        childNode.min_cost_to_connect_reds_with_red_at_root
                        < childNode.cost_to_blackify
                    ):
                        childNode.min_cost_to_connect_reds_with_red_at_root += (
                            childNode.min_cost_to_connect_reds_with_red_at_root
                        )
                        has_children_with_reds = True
                    else:
                        node.min_cost_to_connect_reds_with_red_at_root += (
                            childNode.cost_to_blackify
                        )
                node.min_cost_to_connect_reds_with_red_at_root += (
                    node.weight if has_children_with_reds and node.color == "R" else 0
                )

                node.min_cost_to_connect_reds_unconditional = min(
                    node.cost_to_blackify,
                    node.min_cost_to_connect_reds_with_red_at_root,
                )
            else:
                node.cost_to_blackify = 0

        post_order_traversal(root)

        print(root)
        return 0


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    n: int, colors: str, edges: list[list[int]], expected: int
) -> tuple[bool, str]:
    actual = Solution().minCost(n, colors, edges)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=3, colors="RBR", edges=[[0, 1], [1, 2]], expected=0)
            # Test(n=    , colors =                , edges=                    , expected=         )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
