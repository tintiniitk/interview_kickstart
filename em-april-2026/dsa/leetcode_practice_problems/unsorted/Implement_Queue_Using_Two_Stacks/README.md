# Implement Queue Using Two Stacks
Given a sequence of enqueue and dequeue operations, return a result of their execution without using a queue implementation from a library. Use two stacks to implement queue.

Operations are given in the form of a linked list, and you need to return the result as a linked list, too. Operations:

A non-negative integer means "enqueue me".
-1 means
If the queue is not empty, dequeue current head and append it to the result.
If the queue is empty, append -1 to the result.

## Example One
{
"operations": [1, -1, 2, -1, -1, 3, -1]
}
Output:

[1, 2, -1, 3]
Here is how we would execute the operations and build the result list:

Operation	Queue contents after the operation	Result list after the operation
1	[1]	[]
-1	[]	[1]
2	[2]	[1]
-1	[]	[1, 2]
-1	[]	[1, 2, -1]
3	[3]	[1, 2, -1]
-1	[]	[1, 2, -1, 3]

## Example Two
{
"operations": [0, 1, 2, -1, 3]
}
Output:

[0]
The only dequeue operation results in the first enqueued element, 0, to be appended to the result list.

## Notes

## Constraints:
- -1 <= value in the list of operations <= 2 * 109
- 1 <= number of operations <= 105
- There will be at least one dequeue (-1) operation