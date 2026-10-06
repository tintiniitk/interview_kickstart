class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        if n == 1:
            return [0]

        # Original implementation
        # rev_temperatures = list(reversed(temperatures))
        # # print(f"rev_temperatures={rev_temperatures}")
        # stack = [] # shows every temperarature that is less than its previous day's temperature.
        # num_consecutive_days_with_lte_temperature_reversed = [1]
        # span = 1
        # for i in range(1, n):
        #     prev_temperature = rev_temperatures[i-1]
        #     cur_temperature = rev_temperatures[i]
        #     if cur_temperature < prev_temperature:
        #         stack.append((i-1, span))
        #         span = 1
        #     else:
        #         while True:
        #             if stack:
        #                 prev_breakpoint_index, prev_breakpoint_span = stack[-1]
        #                 prev_breakpoint_temperature = rev_temperatures[prev_breakpoint_index]
        #                 if prev_breakpoint_temperature <= cur_temperature:
        #                     span = i - prev_breakpoint_index + prev_breakpoint_span
        #                     stack.pop()
        #                 else:
        #                     span = i - prev_breakpoint_index
        #                     break
        #             else:
        #                 span = i+1
        #                 break
        #     num_consecutive_days_with_lte_temperature_reversed.append(span)
        # # print(f"num_consecutive_days_with_lte_temperature_reversed={num_consecutive_days_with_lte_temperature_reversed}")
        # num_consecutive_days_with_lte_temperature = num_consecutive_days_with_lte_temperature_reversed[::-1]
        # return [ count if count < n-i else 0 for i, count in enumerate(num_consecutive_days_with_lte_temperature)]

        # Modified implementation to remove array reversals
        stack: list[
            tuple[int, int]
        ] = []  # saves every day (index, span) whose temperature is higher than its previous day, span is the number of consecutive days including itself starting at itself, with equal or less value that itself.
        num_consecutive_future_days_with_lte_temperature = (
            [1] * n
        )  # for every day, the number of consecutive days including itself starting at itself, with temperature equal or less value that its own.
        prev_temperature = temperatures[-1]
        for i in range(n - 2, -1, -1):
            cur_temperature = temperatures[i]
            span = 1
            if cur_temperature < prev_temperature:
                stack.append((i + 1, 1))
                span = 1
            else:
                while True:
                    if stack:
                        prev_breakpoint_index, prev_breakpoint_span = stack[-1]
                        prev_breakpoint_temperature = temperatures[
                            prev_breakpoint_index
                        ]
                        if prev_breakpoint_temperature <= cur_temperature:
                            span = prev_breakpoint_index - i + prev_breakpoint_span
                            stack.pop()
                        else:
                            span = prev_breakpoint_index - i
                            break
                    else:
                        span = n - i
                        break
            num_consecutive_future_days_with_lte_temperature[i] = span
            prev_temperature = cur_temperature
        # print(f"num_consecutive_days_with_lte_temperature={num_consecutive_days_with_lte_temperature}")
        return [
            count
            if count < n - i
            else 0  # count >= n-i means there is no future day with a higher temperature.
            for i, count in enumerate(num_consecutive_future_days_with_lte_temperature)
        ]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(temperatures: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = Solution().dailyTemperatures(temperatures)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                temperatures=[73, 74, 75, 71, 69, 72, 76, 73],
                expected=[1, 1, 4, 2, 1, 1, 0, 0],
            )
            Test(temperatures=[30, 40, 50, 60], expected=[1, 1, 1, 0])
            Test(temperatures=[30, 60, 90], expected=[1, 1, 0])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
