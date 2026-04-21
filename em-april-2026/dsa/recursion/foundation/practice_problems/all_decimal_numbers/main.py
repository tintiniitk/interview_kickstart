import sys


def decimal_strings_internal(n: int, slate: list[str], ret: list[str]):
    if n == len(slate):
        if n > 0:
            ret.append("".join(slate))
        return
    slate[n] = "0"
    decimal_strings_internal(n + 1, slate, ret)
    for i in range(1, 10):
        slate[n] = str(i)
        decimal_strings_internal(n + 1, slate, ret)


def decimal_strings(n: int) -> list[str]:
    slate = [" "] * n
    ret = []
    decimal_strings_internal(0, slate, ret)
    return ret


if __name__ == "__main__":
    n = 5
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    print(f"decimal_strings({n}) = {decimal_strings(n)}")
