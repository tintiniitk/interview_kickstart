class Solution:
    def getMaximumXor(self, nums: list[int], maximumBit: int) -> list[int]:
        n = len(nums)
        m = maximumBit

        MASK = 2**m - 1

        def k_for_num(num: int) -> int:
            return MASK ^ num

        res = [0] * n
        cumulative_xor = nums[0]
        res[0] = k_for_num(cumulative_xor)
        for i in range(1, n):
            cumulative_xor = cumulative_xor ^ nums[i]
            res[i] = k_for_num(cumulative_xor)
        res.reverse()
        return res


def Test(nums: list[int], maximumBit: int, expected: int):
    orig_nums = nums.copy()
    print(f"[RUN]")
    actual = Solution().getMaximumXor(nums, maximumBit)
    assert actual == expected, (
        f"  actual={actual} != expected={expected} for nums={orig_nums}, maximumBit={maximumBit}\n[FAILED]"
    )
    print(f"[DONE]")


Test([0, 1, 1, 3], 2, [0, 3, 2, 3])
Test([2, 3, 4, 7], 3, [5, 2, 6, 5])
