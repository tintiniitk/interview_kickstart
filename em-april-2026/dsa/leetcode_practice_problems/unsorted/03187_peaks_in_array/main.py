"""
from itertools import accumulate
# import time
# from line_profiler import profile
# from utils.time import format_minimal_seconds
class Solution:
    def countOfPeaks(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        n = len(nums)
        # print(f"n={n},nums={nums}")
        is_peak = [
            (1 if (0 < i < n - 1) and (nums[i + 1] < nums[i] > nums[i - 1]) else 0)
            for i in range(n)
        ]
        cumulative_peaks = list(accumulate(is_peak))
        # print(
        #     f"Initially, is_peak={is_peak}, cumulative_peaks={cumulative_peaks}"
        # )

        ret = []
        # prev_time = time.perf_counter()
        for iter, query in enumerate(queries):
            # start_time = time.perf_counter()
            # duration = start_time - prev_time
            # prev_time = start_time
            # print(f"Previous query took {format_minimal_seconds(duration)}")
            # print(f"Processing query#{iter} i.e. {query} ...")

            # @profile
            def process_query(iter, query):
                match query[0]:
                    case 1:
                        li = query[1]
                        ri = query[2]
                        if not (0 <= li <= ri < n):
                            raise ValueError(
                                f"Didn't meet the condition 0 <= li <= ri < n for i,ri=({li, ri})"
                            )
                        ret.append(
                            cumulative_peaks[ri - 1] - cumulative_peaks[li]
                            if ri > li + 1
                            else 0
                        )
                        # ret.append(sum(filter(lambda x: x > 0, is_peak[li + 1 : ri])))
                        return
                    case 2:
                        # avoid unnecessary work
                        if iter == len(queries) - 1:
                            print("Not making any changes as this is the last query")
                            return
                        i = query[1]
                        if not (0 <= i < n):
                            raise ValueError(
                                f"Didn't meet the condition 0 <= i <= n for i={i})"
                            )
                        val = query[2]
                        if nums[i] == val:
                            # print(
                            #     f"nums[{i}] is already = {val}, so nothing more to do ..."
                            # )
                            return
                        nums[i] = val
                        # print(f"nums -> {nums}")
                        if i >= n - 1:
                            # there is no slot at [i]
                            if i > 1:
                                # there is a slot at [i-1] which can now change
                                old_is_peak_i_minus_one = is_peak[i - 1]
                                is_peak[i - 1] = (
                                    1 if nums[i] < nums[i - 1] > nums[i - 2] else 0
                                )
                                # print(f"is_peak -> {is_peak}")
                                delta = is_peak[i - 1] - old_is_peak_i_minus_one
                                if delta != 0:
                                    cumulative_peaks[i - 1] += delta
                                    # print(
                                    #     f"cumulative_peaks -> {cumulative_peaks}"
                                    # )
                        elif i <= 0:
                            # there is no slot at [i]
                            if i < n - 2:
                                # there is a slot at [i+1] which can change itself and [i+2] onwards.
                                old_is_peak_i_plus_one = is_peak[i + 1]
                                is_peak[i + 1] = (
                                    1 if nums[i] < nums[i + 1] > nums[i + 2] else 0
                                )
                                # print(f"is_peak -> {is_peak}")
                                delta = is_peak[i + 1] - old_is_peak_i_plus_one
                                if delta != 0:
                                    for j in range(i + 1, n):
                                        cumulative_peaks[j] += delta
                                    # print(
                                    #     f"cumulative_peaks -> {cumulative_peaks}"
                                    # )
                        # Now, 0 < i < n-1
                        elif 1 < i < n - 2:
                            # there is a slot both at i-1 and at i+1
                            old_is_peak_i_minus_one = is_peak[i - 1]
                            is_peak[i - 1] = (
                                1 if nums[i] < nums[i - 1] > nums[i - 2] else 0
                            )
                            delta_peak_i_minus_one = (
                                is_peak[i - 1] - old_is_peak_i_minus_one
                            )
                            old_is_peak_i = is_peak[i]
                            is_peak[i] = 1 if nums[i - 1] < nums[i] > nums[i + 1] else 0
                            delta_peak_i = is_peak[i] - old_is_peak_i
                            old_is_peak_i_plus_one = is_peak[i + 1]
                            is_peak[i + 1] = (
                                1 if nums[i] < nums[i + 1] > nums[i + 2] else 0
                            )
                            delta_peak_i_plus_one = (
                                is_peak[i + 1] - old_is_peak_i_plus_one
                            )
                            # print(f"is_peak -> {is_peak}")
                            # update cumulative_peaks
                            cumulative_peaks[i - 1] += delta_peak_i_minus_one
                            cumulative_peaks[i] += delta_peak_i + delta_peak_i_minus_one
                            delta = (
                                delta_peak_i
                                + delta_peak_i_minus_one
                                + delta_peak_i_plus_one
                            )
                            if delta != 0:
                                cumulative_peaks[i + 1 : n] = [
                                    x + delta for x in cumulative_peaks[i + 1 : n]
                                ]
                                # for j in range(i + 1, n):
                                #     cumulative_peaks[j] += delta
                            # print(f"cumulative_peaks -> {cumulative_peaks}")
                        elif i > 1:
                            # there is a slot at i and i-1, but not at >= i+1.
                            old_is_peak_i_minus_one = is_peak[i - 1]
                            is_peak[i - 1] = (
                                1 if nums[i] < nums[i - 1] > nums[i - 2] else 0
                            )
                            delta_peak_i_minus_one = (
                                is_peak[i - 1] - old_is_peak_i_minus_one
                            )
                            old_is_peak_i = is_peak[i]
                            is_peak[i] = 1 if nums[i - 1] < nums[i] > nums[i + 1] else 0
                            delta_peak_i = is_peak[i] - old_is_peak_i
                            # print(f"is_peak -> {is_peak}")
                            # update cumulative_peaks
                            cumulative_peaks[i - 1] += delta_peak_i_minus_one
                            delta = delta_peak_i + delta_peak_i_minus_one
                            if delta != 0:
                                for j in range(i, n):
                                    cumulative_peaks[j] += delta
                            # print(f"cumulative_peaks -> {cumulative_peaks}")
                        elif i < n - 2:
                            # there is a slot at i and i+1, but not at <= i-1.
                            old_is_peak_i = is_peak[i]
                            is_peak[i] = 1 if nums[i - 1] < nums[i] > nums[i + 1] else 0
                            delta_peak_i = is_peak[i] - old_is_peak_i
                            old_is_peak_i_plus_one = is_peak[i + 1]
                            is_peak[i + 1] = (
                                1 if nums[i] < nums[i + 1] > nums[i + 2] else 0
                            )
                            delta_peak_i_plus_one = (
                                is_peak[i + 1] - old_is_peak_i_plus_one
                            )
                            # print(f"is_peak -> {is_peak}")
                            # update cumulative_peaks
                            # cumulative_peaks[i] += delta_peak_i
                            delta = delta_peak_i + delta_peak_i_plus_one
                            if delta != 0:
                                for j in range(i + 1, n):
                                    cumulative_peaks[j] += delta
                            # print(f"cumulative_peaks -> {cumulative_peaks}")
                        else:  # if i == 1 and n == 3:
                            old_is_peak_i = is_peak[i]
                            is_peak[i] = 1 if nums[i - 1] < nums[i] > nums[i + 1] else 0
                            # print(f"is_peak -> {is_peak}")
                            delta = is_peak[i] - old_is_peak_i
                            if delta != 0:
                                for j in range(i, n):
                                    cumulative_peaks[j] += delta
                                # print(f"cumulative_peaks -> {cumulative_peaks}")

            process_query(iter, query)
        return ret
"""


class FenwickTree:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        idx = index + 1
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def query(self, index: int) -> int:
        """Returns prefix sum from index 0 to index inclusive."""
        idx = index + 1
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx -= idx & (-idx)
        return total

    def query_range(self, left: int, right: int) -> int:
        if left > right:
            return 0
        return self.query(right) - self.query(left - 1)


class Solution:
    def countOfPeaks(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        n = len(nums)
        tree = FenwickTree(n)

        def check_peak(idx: int) -> int:
            if 0 < idx < n - 1 and nums[idx - 1] < nums[idx] > nums[idx + 1]:
                return 1
            return 0

        # Initial peak status array
        is_peak = [check_peak(i) for i in range(n)]
        for i in range(n):
            if is_peak[i]:
                tree.add(i, 1)

        ret: list[int] = []

        for q_type, arg1, arg2 in queries:
            if q_type == 1:
                li, ri = arg1, arg2
                # Peaks strictly inside subarray nums[li..ri] must exclude boundary endpoints li and ri
                if ri - li < 2:
                    ret.append(0)
                else:
                    ret.append(tree.query_range(li + 1, ri - 1))
            else:
                idx, val = arg1, arg2
                if nums[idx] == val:
                    continue

                # Indices whose peak status might be altered by updating nums[idx]
                affected_indices = [i for i in (idx - 1, idx, idx + 1) if 0 < i < n - 1]

                nums[idx] = val

                # Update peak status in Fenwick Tree for affected indices
                for i in affected_indices:
                    new_val = check_peak(i)
                    delta = new_val - is_peak[i]
                    if delta != 0:
                        is_peak[i] = new_val
                        tree.add(i, delta)

        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import eq_list_int, pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.25, stop_on_tc_failure=True)
def Test(nums: list[int], queries: list[list[int]], expected: int) -> tuple[bool, str]:
    actual = Solution().countOfPeaks(nums, queries)
    # with open("output.py", "w") as f:
    #     f.write(f"output = {actual}")
    return eq_list_int(actual, expected)


from tc_x import tc as tc_x_tc
from tc_y import tc as tc_y_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[3, 1, 4, 2, 5], queries=[[2, 3, 4], [1, 0, 4]], expected=[0])
            Test(
                nums=[4, 1, 4, 2, 1, 5],
                queries=[[2, 2, 4], [1, 0, 2], [1, 0, 4]],
                expected=[0, 1],
            )
            Test(
                nums=[5, 4, 8, 6],
                queries=[[1, 2, 2], [1, 1, 2], [2, 1, 6]],
                expected=[0, 0],
            )
            Test(
                nums=[8, 7, 10],
                queries=[[1, 1, 1], [2, 2, 4], [1, 0, 1], [2, 1, 9], [1, 0, 2]],
                expected=[0, 0, 1],
            )
            Test(
                nums=[9, 7, 5, 8, 9],
                queries=[[2, 0, 2], [1, 0, 3], [1, 3, 3], [2, 3, 5]],
                expected=[1, 0],
            )
            Test(
                nums=[3, 3, 4, 7, 4],
                queries=[
                    [1, 3, 4],
                    [2, 1, 9],
                    [2, 4, 4],
                    [1, 0, 3],
                    [1, 3, 3],
                    [1, 4, 4],
                    [1, 4, 4],
                ],
                expected=[0, 1, 0, 0, 0],
            )
            Test(**tc_x_tc)
            Test(**tc_y_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
