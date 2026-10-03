# Array Product
Given an array of numbers, return an array of the same size where i-th element is the product of all elements except the i-th one.

Calculate the products modulo 10<sup>9</sup> + 7.

Using division is not allowed anywhere in the solution. Using more than constant auxiliary space is not allowed.

## Example
```json
{
"nums": [1, 2, 3, 4, 5]
}
```
Output:
```json
[120, 60, 40, 30, 24]
[(2 * 3 * 4 * 5), (1 * 3 * 4 * 5), (1 * 2 * 4 * 5), (1 * 2 * 3 * 5), (1 * 2 * 3 * 4)] = [120, 60, 40, 30, 24]
```

## Notes

## Constraints:
- 2 <= length of the array <= 100000
- -10<sup>9</sup> <= a number in the array <= 10<sup>9</sup>