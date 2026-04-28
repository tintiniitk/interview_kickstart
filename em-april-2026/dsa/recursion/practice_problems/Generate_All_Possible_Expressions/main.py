"""

Generate All Possible Expressions That Evaluate To The Given Target Value
Given a string s that consists of digits ("0".."9") and target, a non-negative integer, find all expressions that can be built from string s that evaluate to the target.

When building expressions, you have to insert one of the following operators between each pair of consecutive characters in s: join or * or +. For example, by inserting different operators between the two characters of string "12" we can get either 12 (1 joined with 2 or "12") or 2 ("1*2") or 3 ("1+2").

Other operators such as - or ÷ are NOT supported.

Expressions that evaluate to the target but only utilize a part of s do not count: entire s has to be consumed.

Precedence of the operators is conventional: join has the highest precedence, * – medium and + has the lowest precedence. For example, 1 + 2 * 34 = (1 + (2 * (34))) = 1 + 68 = 69.

You have to return ALL expressions that can be built from string s and evaluate to the target.

Example
{
\"s\": "202",
\"target\": 4
}
Output:

[\"2+0+2\", \"2+02\", \"2*02\"]
Same three strings in any other order are also a correct output.

Notes
Order of strings in the output does not matter.
If there are no expressions that evaluate to target, return an empty list.
Returned strings must not contain spaces or any characters other than "0",..., "9", "*", "+".
All returned strings must start and end with a digit.
Constraints:

1 <= length of s <= 13
1 <= target <= 1013

Worst-case inputs:
1. s="0000000000000", target=0

"""

from dataclasses import dataclass
from enum import Enum, auto
import sys


class OpType(Enum):
    PLUS = 2
    MULTIPLY = 3


@dataclass
class Node:
    # explicitly sets the value of this node as either an integer in [0, inf) range, or one of the values defined in OpType
    value: int | OpType


def evaluate(s: str) -> int:
    # convert the entire string to list[Node]
    if len(s) < 1:
        return 0
    # print(f"evaluate called for {s}: ")

    def parse(s) -> list[Node]:
        nodes = list[Node]()
        # assuming that first character is a DIGIT
        if not s[0].isdigit():
            raise ValueError(f"first character of expression {s} is not a digit")
        if not s[-1].isdigit():
            raise ValueError(f"last character of expression {s} is not a digit")
        nodes.append(Node(value=int(s[0])))
        prev_node = nodes[-1]
        for c in s[1:]:
            if c.isdigit():
                next_digit = int(c)
                if isinstance(prev_node.value, int):
                    prev_node.value = (10 * prev_node.value) + next_digit
                else:
                    nodes.append(Node(value=next_digit))
                    prev_node = nodes[-1]
            elif c == "+":
                if isinstance(prev_node.value, int):
                    nodes.append(Node(value=OpType.PLUS))
                    prev_node = nodes[-1]
                else:
                    raise ValueError(
                        f"'+' character of expression {s} preceded by a non-digit character"
                    )
            elif c == "*":
                if isinstance(prev_node.value, int):
                    nodes.append(Node(value=OpType.MULTIPLY))
                    prev_node = nodes[-1]
                else:
                    raise ValueError(
                        f"'+' character of expression {s} preceded by a non-digit character"
                    )
            else:
                raise ValueError(f"Unexpected character: {c}")
        return nodes

    def multply_parse(nodes: list[Node]) -> list[Node]:
        if not isinstance(nodes[0].value, int):
            raise ValueError(f"first node among {nodes} is not a digit")
        if not isinstance(nodes[-1].value, int):
            raise ValueError(f"last node among {nodes} is not a digit")
        if len(nodes) % 2 == 0:
            raise ValueError(f"{nodes} is of even length, should be odd!")
        # print(f"Original set of nodes passed to multiply_parse: {nodes}")
        prev_node = nodes[0]
        # it is assumed that every pair of digit nodes has an op-node between them and vice-versa
        i = 1
        while i < len(nodes) - 1:
            op_node = nodes[i]
            next_digit_node = nodes[i + 1]
            if not isinstance(op_node.value, OpType) or not isinstance(
                next_digit_node.value, int
            ):
                raise ValueError(
                    f"Failed check op_node is OpType OR next_digit_node is int at i={i} in {nodes}"
                )
            if op_node.value == OpType.MULTIPLY:
                prev_node.value *= next_digit_node.value
                del nodes[i : i + 2]
                # print(
                #     f"Reduced set of nodes in multiply_parse after removing the operator-node at [{i}] and next-digit-node at [{i+1}]: {nodes}"
                # )
            else:
                prev_node = next_digit_node
                i = i + 2
        return nodes

    def add_parse(nodes: list[Node]) -> list[Node]:
        if not isinstance(nodes[0].value, int):
            raise ValueError(f"first node among {nodes} is not a digit")
        if not isinstance(nodes[-1].value, int):
            raise ValueError(f"last node among {nodes} is not a digit")
        if len(nodes) % 2 == 0:
            raise ValueError(f"{nodes} is of even length, should be odd!")
        prev_node = nodes[0]
        # it is assumed that every pair of digit nodes has an op-node between them and vice-versa
        i = 1
        while i < len(nodes) - 1:
            op_node = nodes[i]
            next_digit_node = nodes[i + 1]
            if (
                not isinstance(op_node.value, OpType)
                or op_node.value != OpType.PLUS
                or not isinstance(next_digit_node.value, int)
            ):
                raise ValueError(
                    f"Failed check op_node is PLUS OR next_digit_node is int at i={i} in {nodes}"
                )
            prev_node.value += next_digit_node.value
            del nodes[i : i + 2]
        return nodes

    nodes = parse(s)
    # print(f"parsed nodes = {nodes}")
    nodes = multply_parse(nodes)
    # print(f"nodes after multiply parse = {nodes}")
    nodes = add_parse(nodes)
    # print(f"nodes after add parse = {nodes}")
    # print(f"evaluate({s}) = {nodes[0].value}")
    return nodes[0].value


def helper(
    s: str, s_index: int, target: int, slate: list[str], filled: int, ret: list[str]
):
    if s_index >= len(s):
        joined = "".join(slate[:filled])
        if evaluate(joined) == target:
            ret.append(joined)
        return
    # first digit has already been handled by the caller
    # try joining
    slate[filled] = s[s_index]
    helper(s, s_index + 1, target, slate, filled + 1, ret)
    # try adding
    slate[filled] = "+"
    slate[filled + 1] = s[s_index]
    helper(s, s_index + 1, target, slate, filled + 2, ret)
    # try multiplying
    slate[filled] = "*"
    slate[filled + 1] = s[s_index]
    helper(s, s_index + 1, target, slate, filled + 2, ret)


def generate_all_expressions(s: str, target: int) -> list[str]:
    """
    Args:
     s(str)
     target(int64)
    Returns:
     list_str
    """
    # Write your code here.
    if len(s) < 0:
        return []
    ret = []
    helper(s, 1, target, [s[0]] + [" "] * (2 * len(s) - 2), 1, ret)
    return ret


if __name__ == "__main__":
    # # s = "12+3*41+5"
    # # s = "1+2*2*2+11"
    # s = "2+0*2"
    # evaluated = evaluate(s)
    # print(f"s={s}, evaluated={evaluated}")
    s = "202"
    target = 4
    if len(sys.argv) > 2:
        s = sys.argv[1]
        target = int(sys.argv[2])
    expressions = generate_all_expressions(s, target)
    if len(expressions) > 100:
        print(f"s={s}, num={len(expressions)}")
    else:
        print(f"s={s}, num={len(expressions)}, expressions={expressions}")
