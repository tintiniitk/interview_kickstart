class Solution:
    def splitArray(self, nums: list[int]) -> int:
        if not nums:
            return 0
        n = len(nums)
        # print(f"n = {n}")

        # # profiling
        # num_additions = 0
        # num_lookups = 0
        # num_assignments = 0
        # num_comparisons = 0
        # num_multiplications = 0

        if n < 2:
            return abs(nums[0])

        # # profiling
        # num_lookups = num_lookups + 1
        # num_lookups = num_lookups + 1
        # num_additions = num_additions + 1

        compositeSum = nums[0] + nums[1]
        primeSum = 0
        nextPrime = 2

        # # profiling
        # num_comparisons = num_comparisons + 1

        while nextPrime < n:

            # # profiling
            # num_lookups = num_lookups + 1
            # num_additions = num_additions + 1

            primeSum += nums[nextPrime]

            # # profiling
            # num_assignments = num_assignments + 1

            nums[nextPrime] = 0

            # # profiling
            # num_multiplications = num_multiplications + 1

            nextCompositeFactor = 2
            nextComposite = nextPrime * nextCompositeFactor

            # # profiling
            # num_comparisons = num_comparisons + 1

            if nextComposite < n:

                # # profiling
                # num_comparisons = num_comparisons + 1
                # num_lookups = num_lookups + 1
                # num_additions = num_additions + 1

                compositeSum += nums[nextComposite]

                # # profiling
                # num_assignments = num_assignments + 1

                nums[nextComposite] = 0

                # # profiling
                # num_multiplications = num_multiplications + 1
                # num_additions = num_additions + 1

                nextCompositeFactor = nextCompositeFactor + 1
                nextComposite = nextPrime * nextCompositeFactor

            nextPrime = nextPrime + 1

            # # profiling
            # num_lookups = num_lookups + 1
            # num_comparisons = num_comparisons + 2

            while nextPrime < n and nums[nextPrime] == 0:

                # # profiling
                # num_comparisons = num_comparisons + 2
                # num_lookups = num_lookups + 1

                nextPrime = nextPrime + 1

        # print(
        # f"n = {n}, num_additions = {num_additions}, num_lookups = {num_lookups}, num_multiplications = {num_multiplications}, num_assignments = {num_assignments}, num_comparisons = {num_comparisons}"
        # )

        return abs(primeSum - compositeSum)


def main():
    nums = [(i + 1) for i in range(0, 100000)]
    # print(f"nums = {nums}")
    # nums = [2, 3, 4]
    # nums = [-1, 5, 7, 0]
    s = Solution()
    solution = s.splitArray(nums)
    print(f"solution = {solution}")


if __name__ == "__main__":
    main()
