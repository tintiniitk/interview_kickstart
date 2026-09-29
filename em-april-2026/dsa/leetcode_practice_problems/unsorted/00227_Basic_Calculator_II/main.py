class Solution:
    def calculate(self, s: str) -> int:
        expr = []
        last_expr_was_op = True
        # pass 1: parse all numbers, and operators
        for c in s:
            match c:
                case "+" | "-" | "*" | "/":
                    assert expr
                    expr.append(c)
                    last_expr_was_op = True
                case " ":
                    # ignore
                    pass
                case _:
                    i = int(c)
                    if expr and not last_expr_was_op:
                        expr[-1] = 10 * expr[-1] + i
                    else:
                        expr.append(i)
                    last_expr_was_op = False
        # print(f"at the end of pass1: expr={expr}")
        if len(expr) == 1:
            return expr[0]
        # pass 2: evaluate all multiply and divide operators:
        expr2 = [expr[0]]
        for e in expr[1:]:
            match e:
                case "+" | "-" | "*" | "/":
                    expr2.append(e)
                case _:
                    last_op = expr2[-1]
                    # print(f"pass2: e={e}, last_op={last_op}, expr2={expr2}")
                    val = e
                    if len(expr2) > 1 and last_op in {"*", "/"}:
                        expr2.pop()
                        operand1 = expr2[-1]
                        expr2.pop()
                        operand2 = e
                        # print(f"pass2: last_op={last_op}, operand1={operand1}, operand2={operand2}")
                        match last_op:
                            case "*":
                                val = operand1 * operand2
                            case "/":
                                val = operand1 // operand2
                    expr2.append(val)
        # print(f"at the end of pass2: expr2={expr2}")
        if len(expr2) == 1:
            return expr2[0]
        # pass 2: evaluate all add and subtract operators:
        expr = expr2
        expr2 = [expr[0]]
        for e in expr[1:]:
            match e:
                # case '*' | '/':
                #     raise ValueError(f"got a * or / in pass 3 in expr={expr}")
                case "+" | "-":
                    expr2.append(e)
                case _:
                    last_op = expr2[-1]
                    if len(expr2) > 1:
                        expr2.pop()
                        operand1 = expr2[-1]
                        expr2.pop()
                        operand2 = e
                        val = 0
                        match last_op:
                            case "+":
                                val = operand1 + operand2
                            case "-":
                                val = operand1 - operand2
                        expr2.append(val)
        # print(f"at the end of pass3: expr2={expr2}")
        return expr2[0]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: int) -> tuple[bool, str]:
    actual = Solution().calculate(s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="3+2*2", expected=7)
            Test(s=" 3/2 ", expected=1)
            Test(s=" 3+5 / 2 ", expected=5)
            Test(s="1+1/2*3+5-3*2", expected=0)
            Test(s="11+12/5*3234+5678-3435*2344", expected=-8039483)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
