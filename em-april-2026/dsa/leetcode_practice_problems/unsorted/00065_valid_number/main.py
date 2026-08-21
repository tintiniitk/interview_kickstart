import re
import unittest

# Matches an optional sign, a decimal number (with or without integer/fractional parts),
# and an optional exponent part (E or e followed by an optional sign and digits).
NUMBER_MATCHER_REGEX = re.compile(
    r"^" + r"([\+\-])?" + r"((\d+(\.\d*)?)|(\d*\.\d+))" + r"([Ee][\+\-]?\d+)?" + r"$"
)


class Solution:
    def isNumber(self, s: str) -> bool:
        # Handle None and trim surrounding whitespace (LeetCode typically expects trimmed input).
        if s is None:
            return False
        s = s.strip()
        if not s:
            return False

        # Use fullmatch to make intent explicit (equivalent to ^...$ anchors).
        return NUMBER_MATCHER_REGEX.fullmatch(s) is not None


class TestIsNumber(unittest.TestCase):
    def setUp(self) -> None:
        self.solution = Solution()

    def test_examples(self):
        cases = [
            ("+5332.532E-10", True),
            ("--5", False),
            ("", False),
            ("a1.5", False),
            ("-10.E-10", True),
            ("-.1", True),
            ("+00E10", True),
            (".", False),
            ("1.", True),
            ("+1.E-10", True),
            ("-1.E-10", True),
            ("1..5", False),
            ("1.5", True),
            ("1.5e10", True),
            ("1.5e-10", True),
            ("1.5e+10", True),
        ]

        for inp, expected in cases:
            with self.subTest(input=inp):
                self.assertEqual(self.solution.isNumber(inp), expected)


if __name__ == "__main__":
    unittest.main()
