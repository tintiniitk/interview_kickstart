# KMP

Given a text and a pattern, find all occurrences of the pattern in the text. Return start indices of all occurrences in the ascending order.

The problem is named after the string-searching algorithm called KMP (Knuth Morris Pratt).

## Example
```json
{
"text": "Ourbusinessisourbusinessnoneofyourbusiness",
"pattern": "business"
}
```
Output:
```json
[3, 16, 34]
```

## Notes
- Indices in the output are zero-based.
- If the pattern does not occur in the text, return [-1].

## Constraints:
- 1 <= length of the text <= 2 * 105
- 1 <= length of the pattern <= 2 * 105
- Text and pattern may contain lowercase and uppercase letters and digits.