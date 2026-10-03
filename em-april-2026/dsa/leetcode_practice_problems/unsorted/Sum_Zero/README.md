# Sum Zero
Given an array of integers, return any non-empty subarray whose elements sum up to zero.

## Example One
```json
{
"arr": [5, 1, 2, -3, 7, -4]
}
```
Output:
```json
[1, 3]
```
Sum of [1, 2, -3] subarray is zero. It starts at index 1 and ends at index 3 of the given array, so [1, 3] is a correct answer. [3, 5] is another correct answer.

## Example Two
```json
{
"arr": [1, 2, 3, 5, -9]
}
```
Output:
```json
[-1]
```
There is no non-empty subarray with sum zero.

## Notes
- The output is an array of type [start_index, end_index] of a non-empty zero sum subarray; zero-based indices; both start_index and end_index are included in the subarray.
- If there are multiple such subarrays, you can return any.
- If no zero sum subarray is found, return [-1].

## Constraints:
- 1 <= length of the input array <= 5 * 10<sup>5</sup>
- -10<sup>9</sup> <= number in the array <= 10<sup>9</sup>