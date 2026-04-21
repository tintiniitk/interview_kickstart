def helper(
    input: list[str], slate: list[str], done: int, filled: int, ret: list[list[str]]
):
    # print(f"{'.' * done}helper({input},{slate},{done},{filled},{ret})")
    n = len(slate)
    if done == n:
        # if done > 0:
        ret.append("".join(slate[:filled]))
        return
    c = input[0]
    remaining_input = input[1:]
    helper(remaining_input, slate, done + 1, filled, ret)
    slate[filled] = c
    helper(remaining_input, slate, done + 1, filled + 1, ret)


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
    print(f"generate_all_subsets({s}) = {generate_all_subsets(s)}")
