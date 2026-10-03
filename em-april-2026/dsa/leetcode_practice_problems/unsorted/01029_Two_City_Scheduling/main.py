class Solution:
    def twoCitySchedCost(self, costs: list[list[int]]) -> int:
        double_n = len(costs)
        n = double_n // 2
        preferred = []
        num_a_preferred, num_b_preferred = 0, 0
        equals = []
        for i, (acost, bcost) in enumerate(costs):
            if acost < bcost:
                preferred.append((acost - bcost, 0, i))
                num_a_preferred += 1
            elif bcost < acost:
                preferred.append((bcost - acost, 1, i))
                num_b_preferred += 1
            else:
                equals.append(i)
        # preferred is of size 2*n at the most containing tuples [-negative of cost saved by the preferred choice for candidate, choice(0 for city a, 1 for city b), i(index for candidate)]
        # candidates in equals could go to either city.
        cost_of_equals = sum([costs[i][0] for i in equals])
        # print(f"preferred={preferred}, num_a_preferred={num_a_preferred}, num_b_preferred={num_b_preferred}, equals={equals}, cost_of_equals={cost_of_equals}")
        if num_a_preferred <= n and num_b_preferred <= n:
            # send all candidates to their preferred city.
            # print("num_a_preferred <= n and num_b_preferred <= n")
            return (
                sum([costs[i][choice] for _, choice, i in preferred]) + cost_of_equals
            )
        # len(preferred) > n is guaranteed now.
        preferred.sort()
        # print(f"sorted preferred={preferred}")
        total_cost = 0
        num_assignments = [0, 0]
        # assign first n from preferred to the city of their preference
        for _, choice, i in preferred[:n]:
            num_assignments[choice] += 1
            total_cost += costs[i][choice]
        # assign remaining from preferred to preferably the city of their preference if space available
        for _, choice, i in preferred[n:]:
            if num_assignments[choice] >= n:
                choice = 1 - choice
            num_assignments[choice] += 1
            total_cost += costs[i][choice]
        total_cost += cost_of_equals
        return total_cost


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(costs: list[list[int]], expected: int) -> tuple[bool, str]:
    actual = Solution().twoCitySchedCost(costs)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(costs=[[10, 20], [30, 200], [400, 50], [30, 20]], expected=110)
            Test(
                costs=[
                    [259, 770],
                    [448, 54],
                    [926, 667],
                    [184, 139],
                    [840, 118],
                    [577, 469],
                ],
                expected=1859,
            )
            Test(
                costs=[
                    [515, 563],
                    [451, 713],
                    [537, 709],
                    [343, 819],
                    [855, 779],
                    [457, 60],
                    [650, 359],
                    [631, 42],
                ],
                expected=3086,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
