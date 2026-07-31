import re
NUMBER_MATCHER_REGEX = re.compile(r"^" + r"([\+-])?" + r"(([0-9]+(\.[0-9]*)?)|([0-9]*\.[0-9]+))" + r"([Ee][-\+]?[0-9]+)?" + r"$")

class Solution:
    def isNumber(self, s: str) -> bool:
        match = NUMBER_MATCHER_REGEX.search(s)
        if match:
            # print(f"s='{s}', matched_path='{match.group()}'")
            return True
        return False

def Test(input: str, expected_output: bool) -> bool:
    orig_input = "".join(input)
    s = Solution()
    output = s.isNumber(input)
    if output != expected_output:
        print(f"output(={output}) != expected_output(!={expected_output}) for input='{input}'")
        return False
    else:
        print(f"Passed: output={output} for input='{input}'")
    return True

Test("+5332.532E-10", True)
Test("--5", False)
Test("", False)
Test("a1.5", False)
Test("-10.E-10", True)
Test("-.1", True)
Test("+00E10", True)
Test(".", False)
Test("1.", True)
Test("+1.E-10", True)
Test("-1.E-10", True)
Test("1..5", False)
Test("1.5", True)
Test("1.5e10", True)
Test("1.5e-10", True)
Test("1.5e+10", True)