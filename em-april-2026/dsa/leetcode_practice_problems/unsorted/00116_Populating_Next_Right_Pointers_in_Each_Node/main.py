import logging

from utils.logger import create_logger

logger = create_logger(logging.INFO)


# Definition for a Node.
class Node:
    val: int = 0
    left: "Node | None" = None
    right: "Node | None" = None
    next: "Node | None" = None

    def __init__(
        self,
        val: int = 0,
        left: "Node | None" = None,
        right: "Node | None" = None,
        next: "Node | None" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root: "Node | None") -> "Node | None":
        if not root:
            return root
        # My original solution with TC=SC=O(n)
        # prev = (None, -1)
        # q = deque([(root, 0)])
        # while q:
        #     node, level = q.popleft()
        #     if prev[0] and prev[1] == level:
        #         prev[0].next = node
        #     prev = (node, level)
        #     if node.left:
        #         q.append((node.left, level + 1))
        #     if node.right:
        #         q.append((node.right, level + 1))
        # return root

        # Leetcode optimal solution with TC=O(n), SC=O(1)
        leftmost = root
        while leftmost.left:
            head = leftmost
            while head:
                if head.left:
                    head.left.next = head.right
                    if head.next and head.right:
                        head.right.next = head.next.left
                head = head.next
            leftmost = leftmost.left
        return root


import sys
from copy import deepcopy

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(root: "Node | None", expected: dict[int, int]) -> tuple[bool, str]:
    orig_root = deepcopy(root)
    modified_root = Solution().connect(orig_root)

    def check_next(node: Node | None) -> bool:
        if node:
            if not node.next and node.val not in expected:
                return True
            if not node.next:
                logger.error(
                    f"node with value {node.val} didn't get any 'next' assigned, while expected was {expected[node.val]}"
                )
                return False
            if node.val not in expected:
                logger.error(
                    f"node with value {node.val} got next assigned as node with value {node.next.val} while no 'next' was expected for it."
                )
                return False
            if node.next.val != expected[node.val]:
                logger.error(
                    f"node with value {node.val} got next assigned as node with value {node.next.val} while node with value {expected[node.val]} was expected for it."
                )
                return False
            return check_next(node.left) and check_next(node.right)
        return True

    if not check_next(modified_root):
        return False, "Failed to match the next pointer for some node."
    return True, ""


def main():
    try:
        logger.info("Running tests ...")
        with time_limit(5):
            Test(
                root=Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7))),
                expected={2: 3, 4: 5, 5: 6, 6: 7},
            )
            Test(
                root=None,
                expected={},
            )
    except TimeoutException as te:
        logger.error(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
