# Minimum Window Substring
You are given alphanumeric strings s and t. Find the minimum window (substring) in s which contains all the characters of t.

## Example One
```json
{
"s": "AYZABOBECODXBANC",
"t": "ABC"
}
```
Output:
```json
"BANC"
````
The minimum window is "BANC", which contains all letters - 'A' 'B' and 'C'. We cannot find a window of smaller length than "BANC".

## Example Two
```json
{
"s": "BACRDESDFBAER",
"t": "BAR"
}
```
Output:
```
"BACR"
```
Here, we can see that there are 2 smallest windows - "BACR" and "BAER". However, the output is "BACR" because it is the leftmost one.

## Notes
- If no such window exists, return an empty string "".
- If there are multiple minimum windows of the same length, return the leftmost window.

## Constraints:
- 1 <= length of s <= 100000
- 1 <= length of t <= 100000