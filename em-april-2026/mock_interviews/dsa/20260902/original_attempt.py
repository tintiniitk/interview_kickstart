# https://coderbyte.com/editor/sharing:vlN80Ees4

"""
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
You must write an algorithm that runs in O(n) time. You can only use O(1) (changed to O(n) later) space.

Example 1:
Input: nums = [100,4,200,1,3,2] Output: 4 Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
Example 2:
Input: nums = [0,3,7,2,5,8,4,6,0,1] Output: 9
Example 3:
Input: nums = [1,0,1,2] Output: 3
"""

# from collections import defaultdict


class LLNode:
    val: int
    next: "LLNode | None"

    def __init__(self, val: int, next: "LLNode | None" = None):
        self.val = val
        self.next = next


class LL:
    head: LLNode
    tail: LLNode
    size: int

    def __init__(self, head: LLNode | None = None):
        if head is not None:
            self.head = head
            self.tail = head
            self.size = 1

    def add(self, node: LLNode):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1


# def max_consecutive_seq_length(nums)-> int:
#   n = len(nums)
#   lists = defaultdict(list)
#   max_size = 0
#   for num in nums:
#     if num in lists:
#       continue
#     if num-1 in lists:
#       lists[num-1].add(LLNode(num))
#       max_size = max(max_size, lists[num-1].size)
#       lists[num] = lists[num-1]
#       del lists[num-1]
#     else:
#       ll = LL(LLNode(num))
#       lists[num] = ll
#       max_size = max(max_size, 1)
#   return max_size


def max_consecutive_seq_length(nums) -> int:
    n = len(nums)
    max_seq = 0
    unique_nums = set(nums)
    max_num = max(unique_nums)
    min_num = min(unique_nums)
    for num in nums:
        if num not in unique_nums:
            continue
        streak = 1
        unique_nums.remove(num)
        k = num + 1
        while k <= max_num and k in unique_nums:
            streak += 1
            unique_nums.remove(k)
            k += 1
        k = num - 1
        while k >= min_num and k in unique_nums:
            streak += 1
            unique_nums.remove(k)
            k -= 1
        max_seq = max(max_seq, streak)
    return max_seq


print(max_consecutive_seq_length([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
print(max_consecutive_seq_length([5, 3, 2, 9]))
print(max_consecutive_seq_length([1, 0, 1, 2]))
