class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        if numerator == 0:
            return "0"
        sign = (numerator < 0 and denominator > 0) or (
            numerator > 0 and denominator < 0
        )
        numerator = abs(numerator)
        denominator = abs(denominator)
        # now numerator >0, denominator > 0
        # start actual division.
        digits_after_decimal = []
        num_before_decimal, remainder = (
            numerator // denominator,
            numerator % denominator,
        )
        # now process digits after decimal.
        remainder_to_pos = {}
        while remainder > 0:
            # print(f"processing for decimal: remainder={remainder} with digits_after_decimal={digits_after_decimal}")
            # if remainder repeats, then the whole pattern since then will repeat.
            if remainder in remainder_to_pos:
                pos = remainder_to_pos[remainder]
                digits_after_decimal = (
                    digits_after_decimal[:pos]
                    + ["("]
                    + digits_after_decimal[pos:]
                    + [")"]
                )
                break
            remainder_to_pos[remainder] = len(digits_after_decimal)
            remainder *= 10  # next decimal place value will be obtained by multiplying remainder by 10, e.g. if we're doing 1/7, then
            # first decimal place will be decided by (10*1)//7, next by ((10%7)*10)//7 and so on.
            q, remainder = (
                remainder // denominator,
                remainder % denominator,
            )

            digits_after_decimal.append(q)
            # print(f"  => digits_after_decimal={digits_after_decimal}")
        return (
            ("-" if sign and (num_before_decimal > 0 or digits_after_decimal) else "")
            + str(num_before_decimal)
            + (
                "." + "".join(map(str, digits_after_decimal))
                if digits_after_decimal
                else ""
            )
        )


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(numerator: int, denominator: int, expected: str) -> tuple[bool, str]:
    actual = Solution().fractionToDecimal(numerator, denominator)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(numerator=1, denominator=2, expected="0.5")
            Test(numerator=2, denominator=1, expected="2")
            Test(numerator=4, denominator=333, expected="0.(012)")
            Test(numerator=1, denominator=625, expected="0.0016")
            Test(numerator=100, denominator=9, expected="11.(1)")
            Test(numerator=100, denominator=7, expected="14.(285714)")
            Test(numerator=7, denominator=-12, expected="-0.58(3)")
            Test(numerator=0, denominator=-4214, expected="0")
            Test(numerator=4214, denominator=-4214, expected="-1")
            Test(numerator=1, denominator=-5, expected="-0.2")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
