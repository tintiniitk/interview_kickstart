from collections.abc import Callable
from dataclasses import dataclass
from heapq import heappop, heappush
from time import sleep

DEBUGGING = False


def log(
    log_factory: Callable[[], object], nop: bool = False, sleep_duration: float = 0.0
) -> None:
    if DEBUGGING and not nop:
        print(log_factory())
        if sleep_duration > 0.0:
            sleep(sleep_duration)


def move_id_to_move_name(id: int) -> str:
    s: str = "unknown"
    match id:
        case 0:
            s = "up"
        case 1:
            s = "down"
        case 2:
            s = "left"
        case 3:
            s = "right"
        case 4:
            s = "origin"
    return s


@dataclass(slots=True, order=True)
class Entry:
    row: int
    col: int
    turns: int  # num-turns upto this entry.
    last_move_id: int  # 0 for row-, 1 for row+, 2 for col-, 3 for col+, 4 for none

    def __init__(
        self,
        row: int,
        col: int,
        turns: int,
        last_move_id: int,
    ):
        self.row = row
        self.col = col
        self.turns = turns
        self.last_move_id = last_move_id

    def __str__(self) -> str:
        return f"{{[{self.row:2},{self.col:2}], #turns={self.turns}, {move_id_to_move_name(self.last_move_id)}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self):
        yield self.row
        yield self.col
        yield self.turns
        yield self.last_move_id


class Solution:
    def minCost(self, grid: list[list[int]], k: int) -> int:
        assert grid is not None
        assert k >= 0
        m = len(grid)
        assert 1 <= m <= 75
        assert m > k
        n = len(grid[0])
        assert 1 <= n <= 75
        assert n > k
        assert all(0 <= cell <= 1000 for row in grid for cell in row)
        if m > 1 and n > 1 and k == 0:
            return -1
        log(lambda: f"m={m}, n={n}, k={k}")
        INF = 10**9
        next_moves = {
            "prev_row": {
                "delta": [-1, 0],
                "id": 0,
                "condition": lambda row, col: row > 0,
            },
            "next_row": {
                "delta": [1, 0],
                "id": 1,
                "condition": lambda row, col: row < m - 1,
            },
            "prev_col": {
                "delta": [0, -1],
                "id": 2,
                "condition": lambda row, col: col > 0,
            },
            "next_col": {
                "delta": [0, 1],
                "id": 3,
                "condition": lambda row, col: col < n - 1,
            },
        }
        min_cost = [
            [[[INF for _ in range(4)] for _ in range(k + 1)] for _ in range(n)]
            for _ in range(m)
        ]
        # The cost of reaching 0,0 in any number of turns from any direction is always grid[0][0].
        min_cost[0][0][:] = [[grid[0][0] for _ in range(4)]] * (k + 1)
        pq = [(grid[0][0], Entry(0, 0, 0, 4))]
        overall_min_cost = INF
        while pq:
            cost, q_entry = heappop(pq)
            row, col, turns, last_move_id = q_entry
            log(
                lambda cost=cost, q_entry=q_entry: (
                    f"popped {cost}, {q_entry} => q={pq}"
                ),
                sleep_duration=0.1,
                nop=False,
            )

            # avoid this branch if there is already a lower-cost parallel branch.
            if 0 <= last_move_id < 4 and min_cost[row][col][turns][last_move_id] < cost:
                log(lambda: "  Ignored this popped entry as it's outdated", nop=False)
                continue

            if row == m - 1 and col == n - 1:
                # terminal move
                if cost < overall_min_cost:
                    overall_min_cost = cost
                    log(
                        lambda overall_min_cost=overall_min_cost: (
                            f"  Updated overall_min_cost to {overall_min_cost}"
                        )
                    )
                else:
                    log(
                        lambda: "  encounterd terminal case so aboting this branch",
                        nop=False,
                    )
                continue

            for move in next_moves.values():
                move_id = move["id"]
                if move["condition"](row, col):
                    next_cell_row, next_cell_col = (
                        row + move["delta"][0],
                        col + move["delta"][1],
                    )
                    next_cell_cost = grid[next_cell_row][next_cell_col]
                    next_cell_new_min_cost = cost + next_cell_cost
                    if (
                        last_move_id == move_id or last_move_id == 4
                    ):  # same movement-direction or starting-cell
                        # number of turns remains same
                        if (
                            min_cost[next_cell_row][next_cell_col][turns][move_id]
                            > next_cell_new_min_cost
                        ):
                            for ki in range(turns, k + 1):
                                min_cost[next_cell_row][next_cell_col][ki][move_id] = (
                                    min(
                                        min_cost[next_cell_row][next_cell_col][ki][
                                            move_id
                                        ],
                                        next_cell_new_min_cost,
                                    )
                                )
                            appended_entry = Entry(
                                next_cell_row,
                                next_cell_col,
                                turns,
                                move_id,
                            )
                            heappush(pq, (next_cell_new_min_cost, appended_entry))
                            log(
                                lambda next_cell_new_min_cost=next_cell_new_min_cost, appended_entry=appended_entry: (
                                    f"  appended {next_cell_new_min_cost},{appended_entry} => q={pq}"
                                ),
                                nop=True,
                            )
                    elif (
                        turns < k
                        and min_cost[next_cell_row][next_cell_col][turns + 1][move_id]
                        > next_cell_new_min_cost
                    ):  # number of turns increased by 1
                        for ki in range(turns + 1, k + 1):
                            min_cost[next_cell_row][next_cell_col][ki][move_id] = min(
                                min_cost[next_cell_row][next_cell_col][ki][move_id],
                                next_cell_new_min_cost,
                            )
                        appended_entry = Entry(
                            next_cell_row,
                            next_cell_col,
                            turns + 1,
                            move_id,
                        )
                        heappush(pq, (next_cell_new_min_cost, appended_entry))
                        log(
                            lambda next_cell_new_min_cost=next_cell_new_min_cost, appended_entry=appended_entry: (
                                f"  appended {next_cell_new_min_cost},{appended_entry} => q={pq}"
                            ),
                            nop=True,
                        )
        return overall_min_cost


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=5, stop_on_tc_failure=False)
def Test(grid: list[list[int]], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().minCost(grid, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(grid=[[2, 7, 3], [1, 4, 5]], k=1, expected=12)
            Test(grid=[[4, 1, 9], [3, 2, 5], [4, 8, 6]], k=2, expected=20)
            Test(grid=[[1, 9], [3, 4]], k=0, expected=-1)
            Test(grid=[[9, 1, 19], [7, 7, 24], [28, 14, 19]], k=1, expected=72)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
