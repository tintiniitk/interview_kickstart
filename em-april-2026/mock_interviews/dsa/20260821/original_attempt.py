"""
The stock span problem is a financial problem where we have a series of N daily price quotes for a stock and
we need to calculate the span of the stock’s price for all N days. The span Si of the stock’s price on a given day i
is defined as the maximum number of consecutive days just before the given day, for which the price of the stock on the
current day is less than or equal to its price on the given day.
Examples:
Input: N = 7, price[] = [100 80 60 70 60 75 85]
Output: 1 1 1 2 1 4 6
Explanation: Traversing the given input span for 100 will be 1, 80 is smaller than 100 so the span is 1, 60 is smaller
than 80 so the span is 1, 70 is greater than 60 so the span is 2 and so on. Hence the output will be 1 1 1 2 1 4 6.
Input: N = 6, price[] = [10 4 5 90 120 80]
Output:1 1 2 4 5 1
Explanation: Traversing the given input span for 10 will be 1, 4 is smaller than 10 so the span will be 1, 5 is greater
than 4 so the span will be 2 and so on. Hence, the output will be 1 1 2 4 5 1

1 < N <= 10^5
price[i] <= 10^5
"""


def foo(param: list[int]) -> list[int]:
    n = len(param)
    if n == 1:
        return [1]
    # dp = [1] * n
    # for i in range(1, n):
    #   if param[i] >= param[i-1]:
    #     dp[i] = dp[i-1] + 1
    # return dp
    stack = []
    ret = [1] * n
    stack.append(0)
    for i in range(1, n):
        if param[i] >= param[i - 1]:
            if stack:
                if param[i] >= param[stack[-1]]:
                    ret[i] = ret[stack[-1]] + (i - stack[-1])
            else:
                ret[i] = ret[i - 1] + 1
            stack.append(i)
    return ret


actual = foo([100, 80, 60, 70, 60, 75, 85])
print(actual)
assert actual == [1, 1, 1, 2, 1, 4, 6]
actual = foo([10, 4, 5, 90, 120, 80])
print(actual)
assert actual == [1, 1, 2, 4, 5, 1]
