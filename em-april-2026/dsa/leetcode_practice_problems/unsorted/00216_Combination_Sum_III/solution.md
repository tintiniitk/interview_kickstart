# Intuition
We need to find all combinations by (a) including and (b) excluding each number while traversing through the numbers 1...9, aborting if at any point the count goes above k, or sum goes above `n`, and accepting a solution with exactly count=`k` and sum=`n` as a valid combination. This is a tree approach with DFS with backtracking.

# Approach
- Store a list of output `combinations`.
- Create a slate (list of ints) of size k with all 0s. For this slate, we'll track the count of numbers in it, as well as the sum of numbers in it.
- We'll go through each number from 1 to 9 each time, and
  - try including the number, by adding this number to the slate
  - alternatively, try excluding the number, by just skipping to the next number
  - at each iteration, check the following:
    - if `count == k`, and `sum == n`, then use slate as a valid combination, and store it in the
    - Otherwise if `count == k`, abort abort the branch, and backtrack
    - Otherwise if `sum >= n`, abort abort the branch, and backtrack
    - Otherwise if next-number to try > 9, abort abort the branch, and backtrack
- When all numbers have been explored, then return the output combinations.

# Complexity
- Time complexity: O(2<sup>n</sup>)
- Space complexity: `O(n)`

# Code
```python
class Solution:
    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        # output combinations
        combinations = []
        # intermittent current combination
        slate = [0] * k

        def helper(next_num: int, l: int, s: int):
            """run future iteration(s) starting with next_num to be included or not, a slate of current count l, and current sum s.

            Args:
                next_num (int): next number to be included or skipped.
                l (int): number of the elements in the slate currently. When it's k, then slate is full.
                s (int): sum of the elements in the slate currently. When it l is k, and s is n, then slate is a valid combination.
            """
            if l == k:
                if s == n:
                    combinations.append(slate.copy())
                return
            if s >= n:
                return
            if next_num > 9:
                return
            # Try including next number.
            slate[l] = next_num
            helper(next_num + 1, l + 1, s + next_num)
            # Try excluding next number.
            helper(next_num + 1, l, s)

        # First iteration starting with next-number 1, with empty slate.
        helper(1, 0, 0)
        # return all the output combinations formed by the above helper call.
        return combinations
```