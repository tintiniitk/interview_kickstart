class Solution:
    def removeStars(self, s: str) -> str:
        # Simple O(n), (s) solution
        stack = []
        for c in s:
            if c == "*":
                if not stack:
                    raise ValueError(
                        f"stack is empty. Input string '{s}' is not proper."
                    )
                stack.pop()
            else:
                stack.append(c)
        return "".join(stack)


def Test(s: str, expected: str):
    print(f"[RUN]\n  s='{s}', expected_answer='{expected}'")
    actual = Solution().removeStars(s)
    assert actual == expected, f"  actual='{actual}', expected='{expected}'\n[FAILED]"
    print("[DONE]")


Test("leet**cod*e", "lecoe")
Test("erase*****", "")
Test("abc**", "a")
Test("ab**", "")
Test("a*", "")
Test("", "")
