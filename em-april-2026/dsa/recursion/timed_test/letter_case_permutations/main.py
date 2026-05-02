def helper(s: str, index: int, slate: list[str], ret: list[str]):
    if index >= len(s):
        ret.append("".join(slate))
        return
    c = s[index]
    # include same as c
    slate[index] = c
    helper(s, index + 1, slate, ret)
    # include toggle-case of c
    if c.isalpha():
        slate[index] = c.swapcase()
        helper(s, index + 1, slate, ret)


def letter_case_permutations(s: str) -> list[str]:
    """
    Args:
     s(str)
    Returns:
     list_str
    """
    # Write your code here.
    ret = list[str]()
    helper(s, 0, ['.']*len(s), ret)
    return ret

if __name__ == "__main__":
	s= "1g2F"
	print(f"letter_case_permutations({s}) = {letter_case_permutations(s)}")
