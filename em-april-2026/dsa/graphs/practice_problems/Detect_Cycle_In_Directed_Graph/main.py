from collections import deque

DEBUGGING = False


# @profile
def has_cycle(
    number_of_vertices: int, number_of_edges: int, edges: list[list[int]]
) -> bool:
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
        if DEBUGGING:
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
            if DEBUGGING:
                print(f"  {node} marked visited")
            for nxt in out_edges[node]:
                parent_of[nxt] = node
                if is_ancestor_of(nxt, node):
                    if DEBUGGING:
                        print(
                            f"  {node} has {nxt} both as child and as ancestor, so cycle found!"
                        )
                    return True
                q.append(nxt)
                if DEBUGGING:
                    print(f"Pushed in {node}'s child {nxt} with => q={q}")
        return False

    for unvisited in range(n):
        if not visited[unvisited]:
            if DEBUGGING:
                print(
                    # f"Starting a new connected graph starting at {unvisited}, with current visited={visited}"
                    f"Starting a new connected graph starting at {unvisited}"
                )
            if visit(unvisited):
                return True
    return False


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    number_of_vertices: int,
    number_of_edges: int,
    edges: list[list[int]],
    expected: bool,
) -> tuple[bool, str]:
    actual = has_cycle(number_of_vertices, number_of_edges, edges)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from inputA import tc as inputA_tc
from inputX import tc as inputX_tc
from inputY import tc as inputY_tc
from inputZ import tc as inputZ_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                number_of_vertices=10,
                number_of_edges=9,
                edges=[
                    [0, 1],
                    [1, 2],
                    [2, 3],
                    [3, 4],
                    [5, 6],
                    [6, 7],
                    [6, 9],
                    [7, 8],
                    [8, 9],
                ],
                expected=False,
            )

            Test(**inputX_tc)
            Test(**inputY_tc)
            Test(**inputZ_tc)
            Test(**inputA_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
