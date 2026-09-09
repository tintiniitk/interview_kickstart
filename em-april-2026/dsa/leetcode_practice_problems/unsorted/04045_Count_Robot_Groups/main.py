from heapq import heappop, heappush
from itertools import pairwise

from utils.collections.DoublyLinkedList import DLL, DLLNode

DEBUGGING = False


class Solution:
    def countGroups(self, position: list[int], speed: list[int], distance: int) -> int:
        assert position is not None
        assert speed is not None
        n = len(position)
        if n == 1:
            return 1
        assert 1 <= n == len(speed) <= 10**5

        if DEBUGGING:
            print(f"position={position}, speed={speed}, distance={distance}")

        markers = [(p, q) for p, q in zip(position, speed)]
        marker_to_existing_marker = []
        existing_markers = DLL()
        for i, (p, s) in enumerate(markers):
            existing_markers.append(DLLNode(val=(i, p, s)))
            marker_to_existing_marker.append(existing_markers.tail())

        if DEBUGGING:
            print(f"markers = {markers}, existing_markers={existing_markers}")

        INF_TIME = float("inf")
        INVALID_POS = -1
        INVALID_SPEED = -1
        INVALID_MARKER = (INVALID_POS, INVALID_SPEED)

        def is_pos_valid(pos: int) -> bool:
            return pos >= 1 and pos != INVALID_POS

        def is_marker_valid(index: int) -> bool:
            return is_pos_valid(markers[index][0])

        eta_pq = []

        def collision_eta(x: int, y: int) -> float:
            """takes in two markers that may collide and returns which marker will disappear and in how much time."""
            assert 0 <= x < y < n
            marker1 = markers[x]
            marker2 = markers[y]
            pos1 = marker1[0]
            pos2 = marker2[0]
            if pos1 < 0 or pos2 < 0:
                return INF_TIME
            speed1 = marker1[1]
            speed2 = marker2[1]
            if speed1 < 0 or speed2 < 0:
                return INF_TIME
            assert 0 <= pos1 <= pos2 <= 10**9
            assert pos1 != pos2
            if pos2 - pos1 <= distance:
                return 0
            if speed1 > speed2:
                return (pos2 - pos1 - distance) / (speed1 - speed2)
            return INF_TIME

        for marker1_index, marker2_index in pairwise(range(n)):
            eta = collision_eta(marker1_index, marker2_index)
            if eta != INF_TIME:
                heappush(eta_pq, (eta, marker1_index, marker2_index))

        if DEBUGGING:
            print(f"eta_pq = {eta_pq}")

        def merge_x_into_y(x: int, y: int, eta: float):
            assert 0 <= x < y < n
            assert is_marker_valid(x)
            assert is_marker_valid(y)
            assert len(marker_to_existing_marker) == n
            xnode = marker_to_existing_marker[x]
            ynode = marker_to_existing_marker[y]
            assert xnode is not None
            assert ynode is not None

            while True:
                markers[x] = INVALID_MARKER
                returnAfterThis = xnode == existing_markers.head()
                xprevnode = xnode.prev
                existing_markers.remove(xnode)
                merged_into[x] = y
                if DEBUGGING:
                    print(
                        f"  {x} merged into {y} => existing_markers={existing_markers}"
                    )

                if returnAfterThis:
                    break

                # As x gets eliminated by being merged into y, we need
                # to look at the immediate previous valid group before x,
                # to see if it can also be merged into y.
                xnode = xprevnode
                x = xnode.val[0]
                assert is_marker_valid(x)
                eta2 = collision_eta(x, y)
                if eta2 == INF_TIME:
                    break
                if eta2 <= eta:
                    continue
                else:
                    heappush(eta_pq, (eta2, x, y))
                    if DEBUGGING:
                        print(
                            f"  Created new potential to merge  {x} into {y} => eta_pq={eta_pq}"
                        )
                    break

        merged_into = {}
        while eta_pq:
            # look for the next earliest collision:
            eta, merged_index, remaining_index = heappop(eta_pq)
            if DEBUGGING:
                print(
                    f"Considering eta, merged_index, remaining_index = {(eta, merged_index, remaining_index)}"
                )
            if is_marker_valid(merged_index):
                if is_marker_valid(remaining_index):
                    merge_x_into_y(merged_index, remaining_index, eta)
                else:
                    assert remaining_index in merged_into
                    new_remaining_index = merged_into[remaining_index]
                    while new_remaining_index in merged_into:
                        new_remaining_index = merged_into[new_remaining_index]
                    eta2 = collision_eta(merged_index, new_remaining_index)
                    if eta2 != INF_TIME:
                        if eta2 <= eta:
                            merge_x_into_y(merged_index, new_remaining_index, eta)
                        else:
                            heappush(eta_pq, (eta2, merged_index, new_remaining_index))
                            if DEBUGGING:
                                print(
                                    f"  Created new potential to merge  {merged_index} into {new_remaining_index} => eta_pq={eta_pq}"
                                )

        if DEBUGGING:
            print(f"finally, merged_into={merged_into}")
            print(f"finally, existing_markers={existing_markers}")
        return existing_markers.size()


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=5, stop_on_tc_failure=False)
def Test(
    position: list[int], speed: list[int], distance: int, expected: int
) -> tuple[bool, str]:
    actual = Solution().countGroups(position, speed, distance)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(position=[1, 5, 6, 20], speed=[4, 3, 2, 3], distance=1, expected=2)
            Test(position=[1, 5, 9], speed=[3, 2, 2], distance=2, expected=2)
            Test(position=[9], speed=[8], distance=5, expected=1)
            Test(
                position=[677, 711, 942, 960],
                speed=[774, 951, 743, 516],
                distance=27,
                expected=1,
            )
            Test(**tc_x_tc)
            Test(
                position=[162, 432, 535], speed=[68, 560, 409], distance=103, expected=2
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
