from math import floor, log10


def total_num_digits(num: int) -> int:
    assert num >= 0
    return 1 if num <= 0 else floor(log10(num)) + 1


def get_last_k_digits(n: int, k: int) -> int:
    # Example:
    # get_last_k_digits(987654321, 4) -> 4321
    """Returns the integer formed by the last k digits."""
    assert k > 0
    assert n >= 0
    return n % (10**k)


def get_first_k_digits(n: int, k: int) -> int:
    """Returns the integer formed by the first k digits."""
    assert k > 0
    assert n >= 0
    n = abs(n)
    if n == 0:
        return 0
    total_digits = total_num_digits(n)
    if k >= total_digits:
        return n
    return n // (10 ** (total_digits - k))


def digits2num(digits: list[int]) -> int:
    n = 0
    for d in digits:
        n = n * 10 + d
    return n


def num2digits(num: int) -> list[int]:
    return [int(d) for d in str(num)]


def pow_mod_base(x: int, y: int, mod_base: int = 1) -> int:
    assert mod_base > 0
    assert y >= 0
    if y == 0:
        return 1
    if y == 1:
        return x % mod_base
    if x == 0:
        return 0
    if y % 2 == 0:
        return ((pow_mod_base(x, y // 2, mod_base) % mod_base) ** 2) % mod_base
    return (
        (((pow_mod_base(x, y // 2, mod_base) % mod_base) ** 2) % mod_base) * x
    ) % mod_base


def main():
    def test_total_num_digits():
        assert total_num_digits(0) == 1
        assert total_num_digits(1) == 1
        assert total_num_digits(9) == 1
        assert total_num_digits(10) == 2
        assert total_num_digits(99) == 2
        assert total_num_digits(764378353) == 9
        assert total_num_digits(1000000000) == 10
        assert total_num_digits(2247677433) == 10

    def test_get_last_k_digits():
        assert get_last_k_digits(0, 1) == 0
        assert get_last_k_digits(1, 1) == 1
        assert get_last_k_digits(2, 1) == 2
        assert get_last_k_digits(10, 1) == 0
        assert get_last_k_digits(10, 2) == 10

    def test_get_first_k_digits():
        assert get_first_k_digits(10, 1) == 1
        assert get_first_k_digits(10, 2) == 10

    def test_digits2num():
        assert digits2num([1]) == 1
        assert digits2num([1, 2, 3, 4]) == 1234
        assert digits2num([1, 6, 6, 7, 5, 1, 7, 9, 4, 1]) == 1667517941

    def test_num2digits():
        assert num2digits(1) == [1]
        assert num2digits(1234) == [1, 2, 3, 4]
        assert num2digits(1667517941) == [1, 6, 6, 7, 5, 1, 7, 9, 4, 1]

    def test_pow_mod_base():
        assert pow_mod_base(10, 5, 2) == 0
        assert pow_mod_base(2, 3, 5) == 3
        assert pow_mod_base(3, 2, 2) == 1
        assert pow_mod_base(10, 100, 9) == 1
        assert pow_mod_base(100, pow_mod_base(10, 1000, 1000000007), 10) == 0
        assert pow_mod_base(10, 5000000000, 9) == 1

    test_total_num_digits()
    test_get_last_k_digits()
    test_get_first_k_digits()
    test_digits2num()
    test_num2digits()
    test_pow_mod_base()


if __name__ == "__main__":
    main()
