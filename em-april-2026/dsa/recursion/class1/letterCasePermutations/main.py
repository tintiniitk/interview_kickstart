def letterCasePermutationsInternal(s: str, n: int) -> list[str]:
    if n <= 0:
        return [""]
    ret = list[str]()
    c = s[n - 1]
    cVariations = [c]
    if c.isalpha():
        cVariations.append(c.upper() if c.islower() else c.lower())
    for x in letterCasePermutationsInternal(s, n - 1):
        for c in cVariations:
            ret.append(x + str(c))
    return ret


def letterCasePermutations(s: str) -> list[str]:
    return letterCasePermutationsInternal(s, len(s))


if __name__ == "__main__":
    s = "cat"
    print(f"s = {s}, permutations={letterCasePermutations(s)}")
    pass
