import sys


def permutations_internal(input: str, i: int, slate: list[str], ret: list[str]):
    # print(f"{' ' * i}Called permutations_internal({input}, {i}, {slate}, {ret})")
    n = len(slate)
    if i == n:
        if i > 0:
            ret.append("".join(slate))
        return
    # for c in input:
    #     if c not in slate:
    #         slate[i] = c
    #         permutations_internal(input, i + 1, slate, ret)
    #         slate[i] = " "
    for idx, c in enumerate(input):
        slate[i] = c
        permutations_internal(input[:idx] + input[idx + 1 :], i + 1, slate, ret)


def permutations(input: str) -> list[str]:
    n = len(input)
    slate = [" "] * n
    ret = []
    permutations_internal(input, 0, slate, ret)
    return ret


if __name__ == "__main__":
    input = "ba"
    if len(sys.argv) > 1:
        input = str(sys.argv[1])
    print(f"permutations({input}) = {permutations(input)}")
