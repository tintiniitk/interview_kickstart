Number Of Ways To Make Change
-----------------------------
Given a variety of coin denominations existing in a currency system, find the total number of ways a given amount of money can be expressed using coins in that currency system.

**Note**: Assume an infinite supply of coins of every denomination.

Example
-------
```py
{
"coins ": [1, 2, 3],
"amount": 3
}
```
Output: 3

The three ways are:
- Use the coin with denomination 1 three times.
- Use the coin with denomination 3 once.
- Use the coin with denomination 2 once and coin with denomination 1 once.

**Notes**:
Two ways are considered different if they use a different number of coins of any particular denomination.

**Constraints**:
- 1 <= total number of denominations <= 102
- 1 <= denomination of a coin <= 104
- 1 <= amount to be expressed <= 104
