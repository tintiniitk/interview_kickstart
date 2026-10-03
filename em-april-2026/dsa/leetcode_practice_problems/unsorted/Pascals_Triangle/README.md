# Pascals Triangle
Pascal’s triangle is a triangular array of the binomial coefficients. Write a function that takes an integer value n as input and returns a two-dimensional array representing pascal’s triangle.

- pascalTriangleArray is a two-dimensional array of size n * n, where
- pascalTriangleArray[i][j] = BinomialCoefficient(i, j); if j <= i,
- pascalTriangleArray[i][j] = 0; if j > i

## Example
```json
{
"n": 4
}
```
Output:
```json
[
[1],
[1, 1],
[1, 2, 1],
[1, 3, 3, 1]
]
```

## Notes
- All values in the 2D output array result must be modulo with (10<sup>9</sup> + 7) and size of result[i] for 0 <= i < n should be (i + 1) i.e. 0s for pascalTriangleArray[i][j] = 0; if j > i, should be ignored.

## Constraints:
- 1 <= n <= 1700