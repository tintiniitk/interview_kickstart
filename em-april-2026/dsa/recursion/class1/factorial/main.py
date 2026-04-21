def factorial(n: int) -> int:
    print(f" called factorial({n})")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    n = 4
    print(f"factorial({n}) = {factorial(n)}")
