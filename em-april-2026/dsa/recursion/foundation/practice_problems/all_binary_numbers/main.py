import sys


def binary_strings_internal(n: int, slate: list[str], ret: list[str]):
    if n == len(slate):
        if n > 0:
            ret.append("".join(slate))
        return
    slate[n] = "0"
    binary_strings_internal(n + 1, slate, ret)
    slate[n] = "1"
    binary_strings_internal(n + 1, slate, ret)


def binary_strings(n: int) -> list[str]:
    slate = [" "] * n
    ret = []
    binary_strings_internal(0, slate, ret)
    return ret


if __name__ == "__main__":
    n = 5
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    print(f"binary_strings({n}) = {binary_strings(n)}")
