import sys


def number_of_ways(coins, amount):
    """
    Args:
     coins(list_int32)
     amount(int32)
    Returns:
     int32
    """
    # Write your code here.
    if not coins:
        return 0
    coins.sort()
    print(f"coins = {coins}")
    if amount < coins[0]:
        return 0
    if amount == coins[0]:
        return 1
    n = len(coins)
    print(f"n = {n}")
    if n == 1:
        # only one-way possible
        if amount % coins[0] == 0:
            return 1
        # not possible
        return 0
    # confirmed n > 1
    # flag and find if there any duplicates in coins
    if any(i for i in range(n - 1) if coins[i] == coins[i + 1]):
        raise ValueError(f"there are duplicate coins in {coins}")
    if amount < coins[1]:
        # only one-way possible
        if amount % coins[0] == 0:
            return 1
        # not possible
        return 0
    # combinations=set()
    # num_combinations=[0 for _ in range(amount+1)]
    # num_combinations[0] = 1
    combinations = [set() for _ in range(amount + 1)]
    combinations[0].add(tuple([0] * n))
    # print(f"combinations = {combinations}")
    for i in range(1, amount + 1):
        # print(f"i = {i}")
        # find num_combinations[amount] given num_combinations[i] for all i < amount
        # num_combinations_for_i = 0
        for j in range(n):
            # print(f"  j = {j}")
            if coins[j] <= i:
                # print(f"    coins[j] <= i")
                # num_combinations_for_i += num_combinations[i - coins[j]]
                for combination in combinations[i - coins[j]]:
                    new_combination = list(combination)
                    new_combination[j] += 1
                    combinations[i].add(tuple(new_combination))
            else:
                break
        # num_combinations[i] = num_combinations_for_i
        # print(f"Updated num_combinations[{i}] to {num_combinations_for_i}")
        # print(f"Updated combinations[{i}] to {combinations[i]}")
    # return num_combinations[amount]
    return len(combinations[amount])


def main():
    coins = [1, 2, 3]
    amount = 3
    if len(sys.argv) >= 2:
        amount = int(sys.argv[1])
        coins = [int(arg) for arg in sys.argv[2:]]
    num_combinations = number_of_ways(coins, amount)
    print(f"num_combinations = {num_combinations}")


if __name__ == "__main__":
    main()
