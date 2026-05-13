import inputX
import inputY
from collections import deque
from dataclasses import dataclass

# # @dataclass
# class LLNode:
#     value: int
#     next: "LLNode"
#     prev: "LLNode"
#     def __init__(self, value: int):
#         self.value = value
#         self.next = None
#         self.prev = None
#     def __str__(self):
#         ret = f"LL.[{self.value}"
#         cur = self
#         while cur.next:
#             ret += f"->{cur.next.value}"
#             cur = cur.next
#         ret += "]"
#         return ret
#     def __repr__(self):
#         return self.__str__()
# # @dataclass
# class LL:
#     head: LLNode
#     tail: LLNode
#     def __init__(self):
#         self.head = None
#         self.tail = None
#         pass
#     def has(self, value: int) -> bool:
#         if not self.head:
#             return False
#         cur = self.head
#         while cur:
#             if cur.value == value:
#                 return True
#             cur = cur.next
#         return False
#     def append(self, value: int) -> "LL":
#         if not self.has(value):
#             node = LLNode(value)
#             if not self.head:
#                 self.head = node
#                 self.tail = node
#             else:
#                 node.prev = self.tail
#                 self.tail.next = node
#                 self.tail = self.tail.next
#         return self
#     def removeFromEnd(self, value: int) -> "LL":
#         if not self.tail:
#             return self
#         if self.tail.value == value:
#             if self.tail.prev:
#                 self.tail.prev.next = None
#             else:
#                 self.head = None
#             self.tail = self.tail.prev
#         return self
#     def __str__(self):
#         if self.head:
#             return self.head.__str__()
#         else:
#             return "LL.[]"
#     def __repr__(self):
#         return self.__str__()


# @profile
def has_cycle(number_of_vertices, number_of_edges, edges):
    """
    Args:
     number_of_vertices(int32)
     number_of_edges(int32)
     edges(list_list_int32)
    Returns:
     bool
    """
    # Write your code here.
    n = number_of_vertices
    # in_edges=[set() for _ in range(n)]
    out_edges = [set() for _ in range(n)]
    for edge in edges:
        # in_edges[edge[1]].add(edge[0])
        out_edges[edge[0]].add(edge[1])

    visited = [False for _ in range(n)]
    parent_of = dict[int, int]()

    def is_ancestor_of(ancestor: int, descendent: int):
        # if ancestor == 0 and descendent == 0:
            # print(f"parent_of={parent_of}")
        cur = descendent
        while cur in parent_of:
            parent = parent_of[cur]
            if not parent:
                return False
            if parent == ancestor:
                return True
            cur = parent
        return False

    # @profile
    def visit(node: int) -> bool:
        nonlocal parent_of
        parent_of = {node: -1}
        q = deque([node])
        # print(f"Starting a BFS with node={node}, visited={visited} => q={q}")
        print(f"Starting a BFS with node={node}, q={q}")

        while len(q) > 0:
            # print(f"q before popping = {q}")
            node = q.popleft()
            # print(f"Popped ({node}) => q={q}")
            # print(f"Called visit({node}), visited={visited}")
            # print(f"Called visit({node})")
            if visited[node]:
                # print(f"node {node} has already been visited")
                # if is_ancestor_of(node, node):
                #     print(
                #         f"  {node} has itself as its ancestor, so cycle found!"
                #     )
                #     return False
                continue
            visited[node] = True
            print(f"  {node} marked visited")
            for nxt in out_edges[node]:
                parent_of[nxt] = node
                if is_ancestor_of(nxt, node):
                    print(
                        f"  {node} has {nxt} both as child and as ancestor, so cycle found!"
                    )
                    return True
                q.append(nxt)
                print(f"Pushed in {node}'s child {nxt} with => q={q}")
        return False

    for unvisited in range(n):
        if not visited[unvisited]:
            print(
                # f"Starting a new connected graph starting at {unvisited}, with current visited={visited}"
                f"Starting a new connected graph starting at {unvisited}"
            )
            if visit(unvisited):
                return True
    return False


if __name__ == "__main__":
    # n = 10
    # e = 9
    # edges = [[0, 1], [1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [6, 9], [7, 8], [8, 9]]
    # expected_output = False
    input = inputY
    n = input.number_of_vertices
    e = input.number_of_edges
    edges = input.edges
    expected_output = input.expected_output
    cycle = has_cycle(n, e, edges)
    print(f"n={n},e={e},has_cycle={cycle},expected_output={expected_output}")
