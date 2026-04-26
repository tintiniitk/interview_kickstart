
# https://leetcode.com/problems/letter-case-permutation/

"""

Given a string s, you can transform every letter individually to be lowercase or
uppercase to create another string.

Return a list of all possible strings we could create. Return the output in any
order.

Example 1:

Input: s = "a1b2"
Output: ["a1b2","a1B2","A1b2","A1B2"]
Example 2:

Input: s = "3z4"
Output: ["3z4","3Z4"]
Constraints:

1 <= s.length <= 12
s consists of lowercase English letters, uppercase English letters, and digits.

"""

class Solution:
    def helper(self, s: str, slate: list[str], n: int, ret: list[str]):
        # print(f"{'.'*n}Called helper({s}, {slate}, {n}, {ret})")
        if n == len(slate):
            ret.append("".join(slate))
            return

        newChar = s[0]
        slate[n] = newChar
        self.helper(s[1:], slate, n + 1, ret)
        if newChar.isalpha():
            slate[n] = newChar.upper() if newChar.islower() else newChar.lower()
            self.helper(s[1:], slate, n + 1, ret)

    def letterCasePermutation(self, s: str) -> list[str]:
        ret = []
        self.helper(s, [" "] * len(s), 0, ret)
        return ret

if __name__ == "__main__":
	
    input = "a1b2";
    expected_output = ["a1b2", "a1B2", "A1b2", "A1B2"]
    actual_output = Solution().letterCasePermutation(input)
    print(f"expected_output = {expected_output}, actual_output = {actual_output}")
