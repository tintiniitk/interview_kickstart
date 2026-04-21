def fib(n: int) -> int:
    print(f" called fib({n})")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    n = 4
    print(f"fib({n}) = {fib(n)}")
