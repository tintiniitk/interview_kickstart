from math import floor, log10


def total_num_digits(num: int) -> int:
    return 1 if num <= 0 else floor(log10(num)) + 1


def get_last_k_digits(num: int, k: int) -> int:
    # Example:
    # get_last_k_digits(987654321, 4) -> 4321
    """Returns the integer formed by the last k digits."""
    return num % (10**k)


def get_first_k_digits(num: int, k: int) -> int:
    """Returns the integer formed by the first k digits."""
    num = abs(num)
    if num == 0:
        return 0
    total_digits = total_num_digits(num)
    if k >= total_digits:
        return num
    return num // (10 ** (total_digits - k))


def digits2num(digits: list[int]) -> int:
    n = 0
    for d in digits:
        n = n * 10 + d
    return n


def num2digits(num: int) -> list[int]:
    return [int(d) for d in str(num)]


def pow_mod_base(x: int, y: int, mod_base: int) -> int:
    if y == 0:
        return 1
    if y == 1:
        return x
    if x == 0:
        return 0
    if y % 2 == 0:
        return ((pow_mod_base(x, y // 2) % mod_base) ** 2) % mod_base
    return ((((pow_mod_base(x, y // 2) % mod_base) ** 2) % mod_base) * x) % mod_base


def main():
    pass


if __name__ == "__main__":
    main()
