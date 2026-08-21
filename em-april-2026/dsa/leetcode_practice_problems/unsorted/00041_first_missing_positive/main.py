OFFSET = 2**32
MIN_WITH_OFFSET = 2**31


class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        param = nums
        if not param:
            return 1
        min_positive = 0
        max_positive = 0
        for num in param:
            if num > max_positive:
                max_positive = num
            if num > 0 and num < min_positive:
                min_positive = num
        # print(f"min_positive={min_positive}, max_positive={max_positive}")
        if max_positive <= 0 or min_positive > 1:
            return 1
        p = min_positive
        q = max_positive
        n = len(param)
        # print(f"p={p}, q={q}, n={n}")
        for i in range(n):
            if param[i] >= MIN_WITH_OFFSET:
                transformed = param[i] - OFFSET - (p + 1)
            else:
                transformed = param[i] - (p + 1)
            # print(f"i={i}, param[{i}]={param[i]}, transformed={transformed}")
            if (
                transformed < n
                and transformed >= 0
                and param[transformed] < MIN_WITH_OFFSET
            ):
                # print(f"param[{transformed}] = {param[transformed]}+SENTINEL")
                param[transformed] += OFFSET
                # print(f"param={param}+{2**31}")
        for i in range(n):
            transformed = i + p + 1
            if param[i] < MIN_WITH_OFFSET:
                return i + p + 1
        return q + 1


def Test(input: list[int], expected_output: int) -> bool:
    orig_input = input.copy()
    s = Solution()
    output = s.firstMissingPositive(input)
    if output != expected_output:
        print(
            f"output(={output}) != expected_output(={expected_output}) for input={orig_input}"
        )
        return False
    else:
        print(f"Passed case: output={output} for input={orig_input}")
    return True


Test([1, 2, 0], 3)
Test([3, 4, -1, 1], 2)
Test([7, 8, 9, 11, 12], 1)
