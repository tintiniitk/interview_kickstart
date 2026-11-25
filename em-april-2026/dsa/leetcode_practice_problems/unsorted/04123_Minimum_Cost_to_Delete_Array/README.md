# 4123. Minimum Cost to Delete Array

https://leetcode.com/problems/minimum-cost-to-delete-array/

You are given an integer array nums.

In one operation, choose any subarray of the current array with length at least two and delete it. The cost of this operation is the sum of the first and last elements of the chosen subarray.

After each operation, the remaining elements are concatenated in their original order.

Return the minimum total cost required to delete the entire array.

# Example 1:
- Input: nums = [2,-7,3,-5]
- Output: -7
- Explanation:
  - Delete [-7, 3] with cost -7 + 3 = -4. The array becomes [2, -5].
  - Delete [2, -5] with cost 2 + (-5) = -3.
  - The total cost is -4 + (-3) = -7.

## Example 2:
- Input: nums = [4,0,-5,2]
- Output: 1
- Explanation:
  - Delete [0, -5] with cost 0 + (-5) = -5. The array becomes [4, 2].
  - Delete [4, 2] with cost 4 + 2 = 6.
  - The total cost is -5 + 6 = 1.

## Example 3:
- Input: nums = [7,-8,1]
- Output: 8
- Explanation:
  - To delete the entire array, all three elements must be deleted in one operation. Deleting only two elements would leave one element, which cannot be deleted.
  - Deleting [7, -8, 1] costs 7 + 1 = 8.
 
## Constraints:
- 2 <= nums.length <= 10<sup>5</sup>
- -10<sup>9</sup> <= nums[i] <= 10<sup>9</sup>
