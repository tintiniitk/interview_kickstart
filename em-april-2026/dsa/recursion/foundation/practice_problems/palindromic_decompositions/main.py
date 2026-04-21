import sys


def is_palindromic(s: str) -> bool:
    if len(s) < 2:
        return True
    return s[0] == s[-1] and is_palindromic(s[1:-1])


def helper(
    remaining: str,
    n: int,
    slate: list[str],
    lastSegment: str,
    done: int,
    filled: int,
    ret: list[str],
):
    # print(f"{'.' * done}helper({remaining},{n},{slate},{done},{filled},{ret})")
    if n == done:
        if done > 0:
            ret.append("".join(slate[:filled]))
        return
    nextChar = remaining[0]
    if done > 0:
        lastSegmentStr = lastSegment
        if is_palindromic(lastSegmentStr):
            slate[filled] = "|"
            slate[filled + 1] = nextChar
            helper(remaining[1:], n, slate, nextChar, done + 1, filled + 2, ret)
        # print(f"{'.'*(done+1)}lastSegment+nextChar={lastSegmentStr+nextChar)}")
        if done < (n - 1) or is_palindromic(lastSegmentStr + nextChar):
            slate[filled] = nextChar
            helper(
                remaining[1:],
                n,
                slate,
                lastSegmentStr + nextChar,
                done + 1,
                filled + 1,
                ret,
            )
    else:
        slate[filled] = nextChar
        helper(remaining[1:], n, slate, nextChar, done + 1, filled + 1, ret)


def palindromic_decompositions(s: str) -> list[str]:
    ret = []
    helper(s, len(s), [" "] * (2 * len(s) - 1), "", 0, 0, ret)
    return ret


def main():
    s = "nitin"
    if len(sys.argv) > 1:
        s = " ".join(sys.argv[1:])
    print(f"palindromic_decompositions({s}) = {palindromic_decompositions(s)}")
    pass


if __name__ == "__main__":
    main()
