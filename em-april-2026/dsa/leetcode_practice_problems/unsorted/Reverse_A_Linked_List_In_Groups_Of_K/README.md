# Reverse A Linked List In Groups Of K

Given a linked list, reverse every group of k nodes. If there is a remainder (a group of less than k nodes) in the end, reverse that last group, too.

## Example One
{
"head": [1, 2, 3, 4, 5, 6],
"k": 3
}
Output:
[3, 2, 1, 6, 5, 4]
Input list consists of two whole groups of three. In the output list the first three and last three nodes are reversed.

## Example Two
{
"head": [1, 2, 3, 4, 5, 6, 7, 8],
"k": 3
}
Output:
[3, 2, 1, 6, 5, 4, 8, 7]
There are two whole groups of three and one partial group (a remainder that consists of just two nodes). Each of the three groups is reversed in the output.

## Notes
- The function has two parameters: head of the given linked list and k.
- Return the head of the linked list after reversing the groups of nodes in it.

## Constraints:
- 1 <= number of nodes in the list <= 100000
- -2 * 109 <= node value <= 2 * 109
- 1 <= k <= number of nodes
- Cannot use more than constant extra space