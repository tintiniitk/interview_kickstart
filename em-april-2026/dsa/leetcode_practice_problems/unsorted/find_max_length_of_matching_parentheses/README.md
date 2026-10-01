# Longest Substring With Balanced Parentheses
Given a string brackets that only contains characters '(' and ')', find the length of the longest substring that has "balanced parentheses".

## Example One
```json
{
"brackets": "((((())(((()"
}
```
Output:
```json
4
```
Because "(())" is the longest substring with balanced parentheses.

## Example Two
{
"balanced": "()()()"
}
Output:
```json
6
```
The entire string "()()()" has parentheses balanced.

## Notes
- A string is defined as having balanced parentheses if and only if it has an equal number of '(' and ')' and its every prefix has at least as many '('s as ')'s.

## Constraints:
- 1 <= length of brackets <= 10<sup>5<sup>