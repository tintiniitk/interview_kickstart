# Find Median Of A Sorted Circular Linked List
Given a pointer to an arbitrary node in a sorted circular linked list, find the median value of the elements.

## Example One
Given pointer points to the node with value 4.
Output:
6
The sequence is sorted by value so the median value is the middle node. The answer does not depend on the specific node given as input: as long as the list is as pictured, the answer is 6.

## Example Two
Given pointer points to the node with value 4.
Output:
5
If the number of nodes is even, the median is the average of two middle values. This list is sorted in the descending order.

## Notes
If the list has an even number of elements, the median is the average of the two middle elements in the sorted sequence.

## Constraints:
- 1 <= number of elements in the list <= 105
- -2 * 109 <= value in the list <= 2 * 109
- All numbers in the input list are even