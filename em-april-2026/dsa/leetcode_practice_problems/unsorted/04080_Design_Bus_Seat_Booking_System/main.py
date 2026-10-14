class BusBooking:
    seats: list[list[int]]
    num_seats_occupied: int = 0
    total_cost_so_far = 0

    def __init__(self, n: int):
        assert n > 0
        self.seats = [[0 for _ in range(n)] for _ in range(4)]
        self.num_seats_occupied = 0
        self.total_cost_so_far = 0

    def toggle(self, seat: str) -> None:
        seat_row_str = seat[0]
        seat_row_num = ord(seat_row_str) - ord("A")
        seat_row = self.seats[seat_row_num]
        seat_num = int(seat[1:]) - 1
        cur_seat_cost = seat_row[seat_num]
        if cur_seat_cost > 0:  # already occupied, then
            self.total_cost_so_far -= cur_seat_cost
            seat_row[seat_num] = 0
            self.num_seats_occupied -= 1
        else:  # cur_seat_cost == 0
            # is it a middle seat or window seat with the adjacent seat unoccupied:
            cur_seat_cost = 3
            if (
                seat_row_num == 1  # middle seat
                or seat_row_num == 2  # middle seat
                or (
                    seat_row_num == 0 and self.seats[1][seat_num] == 0
                )  # window seat with the adjacent seat unoccupied
                or (
                    seat_row_num == 3 and self.seats[2][seat_num] == 0
                )  # window seat with the adjacent seat unoccupied
            ):
                cur_seat_cost = 1
            seat_row[seat_num] = cur_seat_cost
            self.num_seats_occupied += 1
            self.total_cost_so_far += cur_seat_cost
        # print(
        #     f"toggle({seat}) => self.num_seats_occupied={self.num_seats_occupied}, self.total_cost_so_far={self.total_cost_so_far}"
        # )

    def getTotalTime(self) -> int:
        return self.total_cost_so_far

    def getMinTime(self) -> int:
        return self.num_seats_occupied * 1


# Your BusBooking object will be instantiated and called as such:
# obj = BusBooking(n)
# obj.toggle(seat)
# param_2 = obj.getTotalTime()
# param_3 = obj.getMinTime()©leetcode


def operate(ops: list[str], params: list[list[int | str]]) -> list[int | None]:
    bb = None
    assert ops
    assert params
    assert len(ops) == len(params)
    ret: list[int | None] = []
    for op, param in zip(ops, params):
        match op:
            case "BusBooking":
                assert not bb
                assert param
                n = param[0]
                assert isinstance(n, int)
                bb = BusBooking(n)
                ret.append(None)
            case "toggle":
                assert bb
                assert param
                seat = param[0]
                assert isinstance(seat, str)
                bb.toggle(seat)
                ret.append(None)
            case "getTotalTime":
                assert bb
                assert not param
                ret.append(bb.getTotalTime())
            case "getMinTime":
                assert bb
                assert not param
                ret.append(bb.getMinTime())
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    ops: list[str], params: list[list[int | str]], expected: list[int | None]
) -> tuple[bool, str]:
    actual = operate(ops, params)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                ops=["BusBooking", "toggle", "toggle"],
                params=[[2], ["B2"], ["C2"]],
                expected=[None, None, None],
            )
            Test(
                ops=[
                    "BusBooking",
                    "toggle",
                    "toggle",
                    "getTotalTime",
                    "getMinTime",
                    "toggle",
                    "toggle",
                    "getTotalTime",
                    "getMinTime",
                ],
                params=[[20], ["B3"], ["A3"], [], [], ["C3"], ["D3"], [], []],
                expected=[None, None, None, 4, 2, None, None, 8, 4],
            )
            Test(
                ops=[
                    "BusBooking",
                    "toggle",
                    "toggle",
                    "getTotalTime",
                    "toggle",
                    "toggle",
                    "toggle",
                    "getTotalTime",
                    "getMinTime",
                ],
                params=[[10], ["C7"], ["D7"], [], ["D7"], ["C7"], ["D7"], [], []],
                expected=[None, None, None, 4, None, None, None, 1, 1],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
