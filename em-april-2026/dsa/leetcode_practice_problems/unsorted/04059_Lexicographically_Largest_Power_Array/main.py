from collections.abc import Callable

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


class Solution:
    def largestPower(self, nums: list[int]) -> list[int]:
        n = len(nums)
        power = [0] * 15
        bit = 14
        power_index = 0

        all_set = set(range(n))
        constrained_sets_asc_order_size = [
            (n, all_set)
        ]  # [i] = tuple(size ki, tuple of indices of size ki), sorted on size
        # Each tuple (ki, si) represents the constraint indices si of size ki on the first ki numbers derived from the the previous bit-checks.
        # The constraint (ki, si) represents that the permutation perm of size we're looking, for must have the first ki numbers from the index-set si.
        # E.g. for i=0 is for bit=14 => k1, s1, implies first k1 number have 14th bit set, and s1 are the indices of these k1 numbers in [0,n-1] range.
        # This constraint is important as we need to honour this constraint for bit=13,12,... .
        # Similarly for bit=13, we find (k2, s2) under the ambit of the constraint (k1, s1). For sake of generality, let's assume that k2 < k1.
        # Now, If for say bit=12, we get (k3, s3) that honours the (k2, s2) constraint (which will automatically honour (k1, s1)) and If k3 == k2, then we need to check if
        # any of the k1-k2 numbers in s1-s2 follow the bit=12 constraint.
        # We keep constrained_sets_asc_order_size in sorted order of size. constrained_sets_asc_order_size is at most size 16, so keeping it sorted has no
        # significant n-based impact on time or space complexity.
        log(
            lambda: (
                f"originally, constrained_sets_asc_order_size={constrained_sets_asc_order_size}"
            )
        )
        while bit >= 0:
            log(lambda bit=bit: f"At bit={bit}")
            for i, (constrained_set_size, constrained_set) in enumerate(
                constrained_sets_asc_order_size
            ):
                new_constrained_set = [
                    index for index in constrained_set if nums[index] & (1 << bit)
                ]
                log(
                    lambda constrained_set=constrained_set, new_constrained_set=new_constrained_set: (
                        f"  checking against constrained_set={constrained_set}, found new_constrained_set={new_constrained_set}"
                    )
                )
                new_constrained_set_size = len(new_constrained_set)
                if new_constrained_set_size < constrained_set_size:
                    power[power_index] = new_constrained_set_size
                    if new_constrained_set_size > 0:
                        log(
                            lambda power_index=power_index: (
                                f"    updated power[{power_index}] => {power[power_index]}"
                            )
                        )
                        constrained_sets_asc_order_size = (
                            constrained_sets_asc_order_size[:i]
                            + [(new_constrained_set_size, new_constrained_set)]
                            + constrained_sets_asc_order_size[i:]
                        )
                        log(
                            lambda constrained_sets_asc_order_size=constrained_sets_asc_order_size: (
                                f"    updated constrained_sets_asc_order_size => {constrained_sets_asc_order_size}"
                            )
                        )
                    break
                elif (
                    new_constrained_set_size == constrained_set_size
                    and new_constrained_set_size == n
                ):
                    power[power_index] = new_constrained_set_size
                    log(
                        lambda power_index=power_index: (
                            f"    updated power[{power_index}] => {power[power_index]}"
                        )
                    )
                    break
            bit -= 1
            power_index += 1
        return power


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = Solution().largestPower(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[7, 5], expected=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2])
            Test(nums=[3, 1, 7], expected=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
