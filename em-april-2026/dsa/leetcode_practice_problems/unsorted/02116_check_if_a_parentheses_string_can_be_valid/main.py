class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        n = len(s)
        if n < 1:
            return True
        if n % 2 == 1:
            return False
        if s[0] != "(" and locked[0] == 1:
            return False
        if s[n - 1] != ")" and locked[n - 1] == 1:
            return False
        found_valid = False
        num_opens = 1
        num_closes = 0
        filled = 1
        slate = list(s)
        slate[0] = "("
        slate[n - 1] = ")"
        half = n // 2
        print(
            f"initial before recursion: slate={''.join(slate)}, filled={filled}, n={n}, num_opens={num_opens}, num_closes={num_closes}, half={half}"
        )

        def helper():
            nonlocal found_valid
            nonlocal num_opens
            nonlocal num_closes
            nonlocal filled
            print(
                f"helper called with filled={filled}, num_opens={num_opens}, num_closes={num_closes}, slate={''.join(slate)}"
            )
            if filled == (n - 1):
                print(f"  at terminal case of filled={filled}")
                if (num_opens - num_closes) == 1:
                    found_valid = True
                return
            orig_num_opens = num_opens
            orig_num_closes = num_closes
            orig_filled = filled
            print(
                f"  before starting checking consecutive locked indexes, filled={filled}, (n-1)={n - 1}, locked[filled]={locked[filled]}"
            )
            while (filled < (n - 1)) and (locked[filled] == 1):
                if slate[filled] == "(":
                    num_opens += 1
                else:
                    num_closes += 1
                print(
                    f"  found locked index filled={filled}, with now num_opens={num_opens}, num_closes={num_closes}, half={half}"
                )
                if num_opens > half or num_closes > num_opens:
                    num_opens = orig_num_opens
                    num_closes = orig_num_closes
                    filled = orig_filled
                    return
                filled += 1
            print(
                f"  after handling all the consecutive locked indexes, filled={filled}, num_opens={num_opens}, num_closes={num_closes}, slate={''.join(slate)}"
            )
            if filled == n - 1:
                helper()
                if not found_valid:
                    num_opens = orig_num_opens
                    num_closes = orig_num_closes
                    filled = orig_filled
                return
            # locked[filled] is 0
            slate_filled_orig = slate[filled]
            # try open
            if num_opens < half:
                slate[filled] = "("
                num_opens += 1
                filled += 1
                helper()
                if found_valid:
                    return
                filled -= 1
                num_opens -= 1
            # try close
            if num_closes < num_opens:
                slate[filled] = ")"
                num_closes += 1
                filled += 1
                helper()
                if found_valid:
                    return
                filled -= 1
                num_closes -= 1
            slate[filled] = slate_filled_orig
            num_opens = orig_num_opens
            num_closes = orig_num_closes
            filled = orig_filled

        helper()
        return found_valid


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, locked: str, expected: bool) -> tuple[bool, str]:
    actual = Solution().canBeValid(s, locked)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="", locked="", expected=True)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
