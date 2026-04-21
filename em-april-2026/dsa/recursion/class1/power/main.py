def pow(a: int, p: int, depth: int) -> int:
    print(f"{' ' * depth} called pow({a}, {p})")
    if p <= 0:
        return 1
    if p == 1:
        return a
    if p % 2 == 0:
        return pow(a, p / 2, depth + 1) * pow(a, p / 2, depth + 1)
    else:
        return pow(a, p // 2, depth + 1) * pow(a, p // 2, depth + 1) * a


if __name__ == "__main__":
    a = 2
    p = 5
    depth = 0
    print(f"pow({a}, {p}) = {pow(a,p,depth)}")
