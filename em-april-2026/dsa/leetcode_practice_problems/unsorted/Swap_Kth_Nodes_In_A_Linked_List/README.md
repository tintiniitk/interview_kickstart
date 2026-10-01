# Swap Kth Nodes In A Linked List
Given a linked list and an integer k, swap k-th (1-indexed) node from the beginning, with k-th node from the end.

Note that you have to swap the actual nodes, not just their values.

## Example
```json
{
"head": [1, 2, 3, 4, 7, 0],
"k": 2
}
```
Output:
```json
[1, 7, 3, 4, 2, 0]
```

## Notes
- The function has two parameters: head of the given linked list and k.
- Return the head of the linked list after swapping k-th nodes of given linked list.

## Constraints:
- 1 <= number of nodes in the given list <= 100000
- -2 * 109 <= node value <= 2 * 109
- 1 <= k <= number of nodes
- Try to access nodes of the given list as little as possible