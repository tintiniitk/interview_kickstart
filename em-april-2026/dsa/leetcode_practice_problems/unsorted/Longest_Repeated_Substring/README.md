# Longest Repeated Substring

Find the longest substring that repeats at least twice in the given string.

## Example
```json
{
"s": "efabcdhefhabcdiefi"
}
```
Output:
```json
"abcd"
```
"abcd" repeats twice, "ef" repeats three times, some shorter substrings like "a" repeat, too. "abcd" is the longest of them all.

## Notes
- If multiple repeated substrings are the longest, return any one of them.
- If no substring repeats, return an empty string.

## Constraints:
- 2 <= length of the given string <= 2*105
- Given string consists of lowercase English letters, a-z