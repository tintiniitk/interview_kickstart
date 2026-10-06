# Regex Matcher
Given a text string containing characters only from lowercase alphabetic characters and a pattern string containing characters only from lowercase alphabetic characters and two other special characters '.' and '*'.

Your task is to implement a pattern matching algorithm that returns true if pattern is matched with text otherwise returns false. The matching must be exact, not partial.

**Explanation of the special characters**:
- '.' - Matches a single character from lowercase alphabetic characters.
- '*' - Matches zero or more preceding character. It is guaranteed that '*' will have one preceding character which can be any lowercase alphabetic character or special character '.'. But '*' will never be the preceding character of '*'. (That means "**" will never occur in the pattern string.)
- '.' = "a", "b", "c", ... , "z"
- a* = "a", "aa", "aaa", "aaaa",... or empty string("")
- ab* = "a", "ab", "abb", "abbb", "abbbb", ...

## Example One
```json
{
"text": "abbbc",
"pattern": "ab*c"
}
```
Output:
```json
1
```
Given pattern string can match: "ac", "abc", "abbc", "abbbc", "abbbbc", ...

## Example Two
```json
{
"text": "abcdefg",
"pattern": "a.c.*.*gg*"
}
```
Output:
```json
1
```
".*" in pattern can match "", ".", "..", "...", "....", ... . "g*" in pattern can match "", "g", "gg", "ggg", "gggg", ... .
Now, consider:
'.' at position 2 as 'b',
'.*' at position {4, 5} as "...",
'.*' at position {6,7} as "" and
[g*] at position {8,9} as "".
So, "a.c.*gg*" = "abc...g" where we can write "..." as "def". Hence, both matches.

## Example Three
```json
{
"text": "abc",
"pattern": ".ab*.."
}
```
Output:
```
0
```
If we take 'b*' as "" then also, length of the pattern will be 4 (".a.."). But, given text's length is only 3. Hence, they can not match.

## Notes

## Constraints:
- 0 <= text length, pattern length <= 1000
- text string containing characters only from lowercase alphabetic characters.
- pattern string containing characters only from lowercase alphabetic characters and two other special characters '.' and '*'.
- In pattern string, It is guaranteed that '*' will have one preceding character which can be any lowercase alphabetic character or special character '.'. But '*' will never be the preceding character of '*'.