# Area Under Histogram
You will be given an array heights of height of bars, of size n. You have to answer q queries, where in each query, you will be given left index l and right index r. For each query, return the largest rectangular area possible in a histogram formed using (right - left + 1) bars with array of heights as [heights[left], heights[left + 1], heights[left + 2], ..., heights[right]]. Largest rectangle can be made of a number of contiguous bars. For simplicity, you can assume that all bars have the same width and the width is 1 unit.

## Example One
Histogram Example
```json
{
"heights": [6, 2, 5, 4, 5, 1, 6],
"queries": [
[0, 6]
]
}
```
Output:
```json
[12]
```
1st query: l = 0 and r = 6. The largest rectangle area possible is highlighted in the image above.

## Example Two
```json
{
"heights": [2, 4, 6, 5, 8],
"queries": [
[0, 4],
[3, 3]
]
}
```
Output:
```json
[16, 5]
```
1st query: l = 0 and r = 4. A rectangle of area 16 can be formed using 1st to 4th bar (0-based indexing), that is the largest area that exists between 0 and 4.
2nd query: l = 3 and r = 3. The 3rd (zero based) bar is 5 units tall, so the largest rectangle is 1 * 5 = 5 units.

## Notes

## Constraints:
- 1 <= n <= 2*10<sup>5</sup>
- 1 <= q <= 10
- 1 <= heights[i] <= 10<sup>9</sup>, for all i
- 0 <= l <= r < n for each query.