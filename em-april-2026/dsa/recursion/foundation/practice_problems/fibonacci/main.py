def fibInternal(n: int, b1: int, b2: int, depth: int) -> int:
    print(f"{'.' * (depth - 1)}called fibInternal({n}, {b1}, {b2})")
    if n == 0:
        return b1
    if n == 1:
        return b2
    return fibInternal(n - 1, b2, b1 + b2, depth + 1)


def fib(n: int) -> int:
    return fibInternal(n, 0, 1, 1)


# def fibInternal(n: int, depth: int) -> int:
#     print(f"{'.' * depth}called fibInternal({n})")
#     if n == 0:
#         return 0
#     if n == 1:
#         return 1
#     return fibInternal(n - 1, depth + 1) + fibInternal(n - 2, depth + 1)
#
#
# def fib(n: int) -> int:
#     return fibInternal(n, 0)


if __name__ == "__main__":
    n = 20
    print(f"fib({n}) = {fib(n)}")
