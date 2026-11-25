from heapq import heappop, heappush


class Solution:
    def earliestActivationTimes(
        self, n: int, edges: list[list[int]], requiredSignals: list[int]
    ) -> list[int]:
        outgoingNeighbors = [[] for _ in range(n)]
        for u, v, delay in edges:
            outgoingNeighbors[u].append([v, delay])

        numActiveIncomingNeighbors = [0] * n
        INF = 10**16

        ret = [INF] * n
        ret[0] = 0
        isActive = [False] * n
        isActive[0] = True

        pq = [(0, 0)]  # min-heap of (time_of_signal, node_id)

        # simulation
        while pq:
            t, i = heappop(pq)
            numActiveIncomingNeighbors[i] += 1

            if not isActive[i] or i == 0:  # i == 0 is needed for the first iteration
                if not isActive[i]:
                    if numActiveIncomingNeighbors[i] < requiredSignals[i]:
                        continue  # i doesn't become active here.
                    isActive[i] = True
                    ret[i] = t
                for outgoingNeighbor, delay in outgoingNeighbors[i]:
                    if isActive[outgoingNeighbor]:
                        continue  # this is a cycle. We can't activate ac active node again
                    heappush(pq, (t + delay, outgoingNeighbor))
        return [t if t < INF else -1 for t in ret]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    n: int, edges: list[list[int]], requiredSignals: list[int], expected: list[int]
) -> tuple[bool, str]:
    actual = Solution().earliestActivationTimes(n, edges, requiredSignals)
    if actual != expected:
        return (
            False,
            f"got={truncate_param(actual)}, wanted={truncate_param(expected)}",
        )
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                n=3,
                edges=[[0, 1, 1], [0, 2, 1]],
                requiredSignals=[1, 1, 2],
                expected=[0, 1, -1],
            )
            Test(
                n=4,
                edges=[[0, 1, 1], [0, 2, 1], [1, 3, 2], [2, 3, 2]],
                requiredSignals=[3, 1, 1, 2],
                expected=[0, 1, 1, 3],
            )
            Test(
                n=4,
                edges=[[0, 1, 2], [1, 2, 3], [0, 2, 5], [2, 3, 1]],
                requiredSignals=[3, 1, 2, 1],
                expected=[0, 2, 5, 6],
            )
            Test(
                n=4,
                edges=[[0, 1, 2], [1, 0, 1], [1, 2, 1], [2, 3, 1], [3, 2, 1]],
                requiredSignals=[3, 1, 2, 1],
                expected=[0, 2, -1, -1],
            )
            Test(
                n=5,
                edges=[[0, 3, 29], [4, 3, 2], [0, 4, 5]],
                requiredSignals=[1, 1, 1, 2, 1],
                expected=[0, -1, -1, 29, 5],
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
