import logging
from collections import Counter

from utils.logger import create_logger

DEBUGGING = False
logger = create_logger(logging.DEBUG if DEBUGGING else logging.INFO)


class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        ret = []
        if candidates.count(target) > 0:
            ret.append([target])
        if len(candidates) == 1:
            return ret
        # now we'll only look for subsets/combinations of size 2 or more.
        # ignore candidates which are >= target as they can't be a part of a combination of size 2 or more as all candidates are >= 1.
        candidates = [candidate for candidate in candidates if candidate < target]
        freq = Counter(candidates)
        unique_candidates = sorted(set(candidates))
        num_unique_candidates = len(unique_candidates)
        logger.debug(
            f"initially, target={target}, ret={ret}, candidates={candidates}, freq={freq}, unique_candidates={unique_candidates}, num_unique_candidates={num_unique_candidates}"
        )
        slate = []

        level = 1

        def helper(index: int, s: int):
            nonlocal ret
            nonlocal slate
            if DEBUGGING:
                nonlocal level
                level += 1
            if s == target:
                ret.append(slate.copy())
                # logger.debug(f"{'  ' * level}ret = {ret}")
                if DEBUGGING:
                    level -= 1
                return
            if index == num_unique_candidates:
                if DEBUGGING:
                    level -= 1
                return
            u = unique_candidates[index]
            logger.debug(
                f"{'  ' * level}helper(u={unique_candidates[index]}, s={s}) with {''.join(list(map(str, slate))) if slate else "''"}"
            )
            if s + u > target:
                if DEBUGGING:
                    level -= 1
                return
            for i in range(freq[u] + 1):
                if s + i * u <= target:
                    slate.extend([u] * i)
                    helper(index + 1, s + i * u)
                    for _ in range(i):
                        slate.pop()
                else:
                    break
            if DEBUGGING:
                level -= 1

        helper(0, 0)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    candidates: list[int], target: int, expected: list[list[int]]
) -> tuple[bool, str]:
    actual = Solution().combinationSum2(candidates, target)
    if sorted(map(tuple, actual)) != sorted(map(tuple, expected)):
        return False, f"got={truncate_param(actual)}, wanted={truncate_param(expected)}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        logger.info("Running tests ...")
        with time_limit(5):
            Test(
                candidates=[10, 1, 2, 7, 6, 1, 5],
                target=8,
                expected=[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]],
            )
            Test(candidates=[2, 5, 2, 1, 2], target=5, expected=[[1, 2, 2], [5]])
            Test(**tc_x_tc)
    except TimeoutException as te:
        logger.error(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
