import sys


def helper(
    s: list[str], slate: list[str], done: int, filled: int, ret: list[list[str]]
):
    # print(f"{'.' * done}helper({s},{slate},{done},{filled},{ret})")
    n = len(slate)
    if done == n:
        # if done > 0:
        ret.append("".join(slate[:filled]))
        return
    helper(s[1:], slate, done + 1, filled, ret)
    slate[filled] = s[0]
    helper(s[1:], slate, done + 1, filled + 1, ret)


def generate_all_subsets(s):
    """
    Args:
     s(str)
    Returns:
     list_str
    """
    # Write your code here.
    ret = []
    helper(list(s), [" "] * len(s), 0, 0, ret)
    return ret


if __name__ == "__main__":
    s = "okmijnuhbyg"
    if len(sys.argv) > 1:
        s = str(sys.argv[1])
    print(f"generate_all_subsets({s}) = {generate_all_subsets(s)}")
