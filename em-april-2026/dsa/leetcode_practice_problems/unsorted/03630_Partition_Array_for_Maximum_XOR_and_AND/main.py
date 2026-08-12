from typing import List


class Solution:
    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)

        res = 0
        count_a, count_b, count_c = 0, 0, 0
        xor_a, and_b, xor_c = 0, 0, 0

        num_helper_calls = 0
        num_combinations_tried = 0

        def helper():
            nonlocal count_a
            nonlocal count_b
            nonlocal count_c
            nonlocal xor_a
            nonlocal and_b
            nonlocal xor_c
            nonlocal res
            nonlocal num_helper_calls
            nonlocal num_combinations_tried

            # if not (num_helper_calls % 2000000):
            #     print(f"num_helper_calls = {num_helper_calls}")
            num_helper_calls += 1

            count = count_a + count_b + count_c
            if count == n:
                num_combinations_tried += 1
                new_res = xor_a + xor_c + and_b
                if new_res > res:
                    res = new_res
                    print(
                        f"num_combinations_tried={num_combinations_tried} => count_a={count_a}, count_b={count_b}, count_c={count_c}, res = {new_res}"
                    )
                elif not (num_combinations_tried % 1000000):
                    print(f"num_combinations_tried={num_combinations_tried}")
                return
            val = nums[count]
            # go to a
            orig_xor_a = xor_a
            if count_a == 0:
                xor_a = val
            else:
                xor_a = xor_a ^ val
            count_a += 1
            helper()
            count_a -= 1
            xor_a = orig_xor_a
            # go to b
            orig_and_b = and_b
            if count_b == 0:
                and_b = val
            else:
                and_b = and_b & val
            count_b += 1
            helper()
            count_b -= 1
            and_b = orig_and_b
            # go to c
            orig_xor_c = xor_c
            if count_c == 0:
                xor_c = val
            else:
                xor_c = xor_c ^ val
            count_c += 1
            helper()
            count_c -= 1
            xor_c = orig_xor_c
            return

        num_helper_calls = 0
        num_combinations_tried = 0
        helper()
        return res


def Test(nums: List[int], expected: int):
    print(f"[RUN]")
    actual = Solution().maximizeXorAndXor(nums)
    assert (
        actual == expected
    ), f"  actual(={actual}) != expected(={expected}) for nums={nums}\n[FAILED]"
    print(f"[DONE]")


# Test([2, 3], 5)
# Test([1, 3, 2], 6)
# Test([2, 3, 6, 7], 15)
# Test(list(range(1, 20)), 15)
Test(list(range(1, 10)) + list(range(10**9, 10**9 - 10, -1)), 15)
