r"""

Longest Path In Weighted DAG
Given a weighted directed acyclic graph (DAG), find the longest path between two nodes.

Example
Example one

{
"dag_nodes": 4,
"dag_from": [1, 1, 1, 3],
"dag_to": [2, 3, 4, 4],
"dag_weight": [2, 2, 4, 3],
"from_node": 1,
"to_node": 4
}
Output:

[1, 3, 4]
Total there are two paths from node 1 to node 4:

1 -> 4 with length 4.
1 -> 3 -> 4 with length 2 + 3 = 5.
The latter is the longest one.

Notes:
The first four arguments of the function - dag_nodes, dag_from, dag_to, dag_weight - together define the given weighted DAG:
  there are dag_nodes nodes and there is an edge from dag_from[i] node to dag_to[i] node with length dag_weight[i] for 0 <= i <= dag_nodes - 1.
Return an array of integers, the nodes in the longest paths from from_node to to_node (including both ends).
If from_node = to_node, return [from_node].
If there are multiple longest paths, return any one.

Constraints:
 There will be at most one edge connecting any pair of nodes in one direction, i.e. no multi edges.
 to_node is reachable from from_node.\
 l <= dag_nodes <= 450
 1 <= dag_from[i], dag_to[i], from_node, to_node <= dag_nodes
 1 <= dag_weight[i] <= 2 * 109
 Total number of edges in the graph <= (dag_nodes * (dag_nodes - 1)) / 2
"""

# from heappq import heappush_max, heappop_max


def find_longest_path(dag_nodes, dag_from, dag_to, dag_weight, from_node, to_node):
    """
    Args:
     dag_nodes(int32)
     dag_from(list_int32)
     dag_to(list_int32)
     dag_weight(list_int32)
     from_node(int32)
     to_node(int32)
    Returns:
     list_int32
    """
    # Write your code here.
    n = dag_nodes
    if n < 1:
        return []
    if n < 2:
        return [to_node]

    # sanity testing and edge-cases
    if from_node < 1 or from_node > n:
        raise ValueError(f"from_node < 1 or from_node > n")
    if to_node < 1 or to_node > n:
        raise ValueError(f"to_node < 1 or to_node > n")
    if any(dag_from_node < 1 or dag_from_node > n for dag_from_node in dag_from):
        raise ValueError(f"dag_from_node < 1 or dag_from_node > n")
    if any(dag_to_node < 1 or dag_to_node > n for dag_to_node in dag_to):
        raise ValueError(f"dag_to_node < 1 or dag_to_node > n")
    if to_node == from_node:
        return [to_node]

    # # make every node-value 0-based
    # dag_from = [i - 1 for i in dag_from]
    # dag_to = [i - 1 for i in dag_to]
    # from_node -= 1
    # to_node -= 1

    # print initial debug info
    print(f"Inputs:")
    print(f"n={n}")
    print(f"from_node={from_node}")
    print(f"to_node={to_node}")
    print(f"dag_from={dag_from}")
    print(f"dag_to={dag_to}")
    print(f"dag_weight={dag_weight}")

    # create in/out-lists
    e = len(dag_from)
    if e != len(dag_to):
        raise ValueError(f"len(dag_from)={e} != len(dag_to)={len(dag_to)}")
    if e != len(dag_weight):
        raise ValueError(f"len(dag_from)={e} != len(dag_weight)={len(dag_weight)}")
    if e < 1:
        return 0
    out_lists = [set() for _ in range(n + 1)]
    # in_lists=[set() for _ in range(n+1)]
    edge_weights = [dict[int, int]() for _ in range(n + 1)]
    for i in range(e):
        out_lists[dag_from[i]].add(dag_to[i])
        # in_lists[dag_to[i]].add(dag_from[i])
        edge_weights[dag_from[i]][dag_to[i]] = dag_weight[i]

    print(f"Derivative variables:")
    print(f"out_lists={out_lists}")
    print(f"edge_weights={edge_weights}")

    # iterative DFS
    visiting = [False for _ in range(n + 1)]
    path_so_far = []  # an ordered version of visiting
    max_weight_to_to_node = 0
    max_weight_path_to_node = [to_node]
    weight_so_far = 0
    stack = [(from_node, False)]
    # visited = [False for _ in range(n + 1)]
    while stack:
        node, backtracked = stack.pop()
        print(
            f"Popped ({node:>2}, {str(backtracked):>5}) from stack. "
            f"path_so_far={str(path_so_far):<15}, " # visiting={str([node for node in range(1,n+1) if visiting[node]]):<15},  
            f"max_weight_to_to_node={max_weight_to_to_node}, max_weight_path_to_node={str(max_weight_path_to_node):<15} => stack={str(stack):<20}"
        )
        # print(
        #     f"Popped {node:>2}, {str(backtracked):>5} from stack => {str(stack):<20}"
        #     f", visiting={str([node for node in range(1,n+1) if visiting[node]]):<15}, path_so_far={str(path_so_far):<15}"
        # )
        if backtracked:
            visiting[node] = False
            # print(f"{node} removed from visiting")
            # visited[node] = True
            # print(f"{node} marked as visited")
            if not path_so_far or len(path_so_far) == 0:
                raise ValueError(
                    f"Error: path_so_far is empty while backtracking a node !"
                )
            if path_so_far[-1] != node:
                raise ValueError(
                    f"Error: While backtracking node {node}, it is not the last in current path_so_far={path_so_far} !"
                )
            path_so_far.pop()
            if len(path_so_far) > 1:
                prev_visited_node = path_so_far[-1]
                if node in edge_weights[prev_visited_node]:
                    weight_so_far -= edge_weights[prev_visited_node][node]
                else:
                    raise ValueError(
                        f"Error: While removing backtracked node {node}, there is no edge to prev visited node {prev_visited_node} !"
                    )
            continue
        if visiting[node]:
            # hit cycle. ignore it.
            print(f"Warning: found cycle while visiting {node:>2}, ignoring it...")
            continue
        # if visited[node]:
        #     print(f"Warning: visiting {node:>2} again when it's already marked visited, ignoring it...")
        #     # hit the same node again. ignore it this time.
        #     continue
        if node == to_node:
            if not path_so_far or len(path_so_far) == 0:
                continue
            prev_node = path_so_far[-1]
            total_weight_so_far = weight_so_far + edge_weights[prev_node][to_node]
            prefix = f"Ended up at final node {to_node}, with path_so_far={path_so_far}, and total_weight_so_far={total_weight_so_far}"
            if total_weight_so_far > max_weight_to_to_node:
                max_weight_to_to_node = total_weight_so_far
                max_weight_path_to_node = path_so_far + [to_node]
                print(
                    f"Debug: {prefix} and updated max_weight_to_to_node=>{max_weight_to_to_node} and max_weight_path_to_node=>{max_weight_path_to_node}"
                )
            else:
                print(
                    f"Debug: {prefix} but failed to update max_weight_to_to_node and max_weight_path_to_node"
                )
            continue
        if len(path_so_far) > 0:
            prev_visited_node = path_so_far[-1]
            if node in edge_weights[prev_visited_node]:
                weight_so_far += edge_weights[prev_visited_node][node]
            else:
                print(
                    f"Warning: Visited node {node} after {prev_visited_node}, but there is no known weight from {prev_visited_node} to {node} !"
                )
                continue
        visiting[node] = True
        stack.append((node, True))
        print(f"Pushed {node:>2},  True to stack => {str([node for node, backtracking in stack]):<20}")
        path_so_far.append(node)
        for nxt_node in out_lists[node]:
            if not visiting[nxt_node]:
                stack.append((nxt_node, False))
                print(f"Pushed {nxt_node:>2}, False to stack => {str([node for node, backtracking in stack]):<20}")
                # print(f"Pushed {nxt_node:>2} to stack => {str(stack):<20}")

    # return [node+1 for node in max_weight_path_to_node]
    return [node for node in max_weight_path_to_node]


def main():
    # # test case 1
    # dag_nodes=4
    # dag_from= [1, 1, 1, 3]
    # dag_to= [2, 3, 4, 4]
    # dag_weight= [2, 2, 4, 3]
    # from_node= 1
    # to_node=4

    # test case 2
    dag_nodes = 5
    dag_from = [5, 4, 3, 2, 5, 5, 3]
    dag_to = [4, 3, 2, 1, 1, 3, 1]
    dag_weight = [1, 1, 1, 1, 3, 3, 1]
    from_node = 5
    to_node = 1

    output_path = find_longest_path(
        dag_nodes, dag_from, dag_to, dag_weight, from_node, to_node
    )
    print(f"from_node={from_node}, to_node={to_node}, output_path = {output_path}")


if __name__ == "__main__":
    main()
