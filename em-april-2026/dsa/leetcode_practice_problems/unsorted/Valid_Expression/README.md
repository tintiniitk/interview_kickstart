# Valid Expression
You have to check whether a given string is a valid mathematical expression or not. A string is considered valid if it contains matching opening and closing parenthesis as well as valid mathematical operations. The string contains the following set of parentheses ‘(‘, ’)’, ’[’, ’]’, ’{’, ’}’, numbers from 0 to 9 and following operators ‘+’, ’-’ and ‘*’.

## Example One
```json
{
"expression": "{(1+2)*3}+4"
}
```
Output:
```json
1
```
The mathematical expression as well as the parentheses are valid.

## Example Two
```json
{
"expression": "((1+2)*3*)"
}
```
Output:
```json
0
```
Here the parentheses are valid but the mathematical expression is not. There is an operator ‘*’ without any operand after it.

## Notes
An expression that consists of only parentheses is considered valid if it contains correct opening and closing parentheses. Example: “{()}” is considered valid.

## Constraints:
- 1 <= length of the expression <= 100000
- Possible characters in the expression string: ‘+’, ‘-’, ‘*’ and [0-9]
