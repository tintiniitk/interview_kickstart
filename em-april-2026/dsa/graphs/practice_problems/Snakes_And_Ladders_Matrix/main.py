"""
Snakes And Ladders Matrix
Find the minimum number of die rolls necessary to reach the final cell of the given Snakes and Ladders board game.

Rules are as usual. Player starts from cell one, rolls a die and advances 1-6 (a random number of) steps at a time. Should they land on a cell where a ladder starts, the player immediately climbs up that ladder. Similarly, having landed on a cell with a snake’s mouth, the player goes down to the tail of that snake before they roll the die again. Game ends when the player arrives at the last cell.

The function has two input arguments:

n, size of the board, and
moves, array of integers defining the snakes and ladders:
moves[i] = -1: no ladder or snake starts at i-th cell
moves[i] < i: snake from i down to moves[i]
moves[i] > i: ladder from i up to moves[i]
The indices and values in moves array are zero-based, for example moves[1] = 18 means there is a ladder from cell 2 up to cell 19.

Example One
{
\"n\": 20,
\"moves\": [-1, 18, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1]
}
Output:

2
Example image

A board with 20 cells, two ladders 2->19 and 13->16, and a snake 9->3.

Note that the two-dimensional view is for our visual convenience only: there are really just 20 cells, one after another, linearly.

Having started from cell 1, the player rolls 1 and moves to cell 2. The ladder takes them from cell 2 to cell 19. They don't roll the die again since they've already reached the final cell. The player reached the end of the board in just one roll after climbing the ladder, that’s the fewest rolls possible.

Example Two
{
\"n\": 8,
\"moves\": [-1, -1, -1, -1, -1, -1, -1, -1]
}
Output:

2
Example two

A board with eight cells, no snakes and no ladders.

There are several ways to reach the last cell from the first cell in two rolls: 6+1, 5+2, 4+3, 3+4, 2+5, 1+6. No way to reach it with any fewer rolls though.

Notes
Return -1 if the last cell cannot be reached.
Constraints:

1 <= n <= 105
0 <= moves[i] <= n - 1
No snake starts from the last cell and no ladder starts from the first cell.
No snake or ladder starts from a cell where another snake or ladder arrives.
"""

import sys
from line_profiler import profile
import test00
import test01
import test02
import test03
import test04
import test05
import test06
import test07
import test08
import test09
import test10

DICE_SIZE = 6
TYPE_SNAKE = 2
TYPE_LADDER = 1
TYPE_NORMAL = 0


@profile
def minimum_number_of_rolls(n, moves):
    """
    Args:
     n(int32)
     moves(list_int32)
    Returns:
     int32
    """
    # Write your code here.
    if n <= 1:
        return 0

    if n != len(moves):
        raise ValueError(f"n={n} != len(moves)={len(moves)}")
    if n <= (DICE_SIZE + 1):
        return 1
    last = n - 1

    types = [
        (
            TYPE_NORMAL
            if (moves[i] == -1)
            else (TYPE_LADDER if (moves[i] > i) else TYPE_SNAKE)
        )
        for i in range(n)
    ]
    # print(f"types={types}")
    snakes = [
        (i, moves[i]) for i in range(n) if types[i] == TYPE_SNAKE
    ]  # list of (snake_head,snake_tail)
    print(f"snakes={snakes}")
    ladders = [
        (i, moves[i]) for i in range(n) if types[i] == TYPE_LADDER
    ]  # list of (ladder_base,ladder_tail)
    print(f"ladders={ladders}")

    @profile
    def has_no_path():
        # there is no path if there are 6 consecutive snake heads without any ladders across it
        if n >= (DICE_SIZE + 1):
            snake_pits = []
            cur = -1
            for snake_head, snake_tail in snakes:
                if snake_head <= cur:
                    continue
                cur = snake_head + 1
                while cur < n and types[cur] == TYPE_SNAKE:
                    cur = cur + 1
                if cur - snake_head >= DICE_SIZE:
                    cur_snake_pit = (snake_head, cur - 1)
                    snake_pits.append(cur_snake_pit)
            # consecutive_snake_positions=[x for x,tail in snakes if (x < (n-DICE_SIZE) and all(types[x+i] == TYPE_SNAKE for i in range(1,DICE_SIZE)))]
            print(f"snake_pits={snake_pits}")
            # check for each snake_pit
            for snake_pit_start, snake_pit_end in snake_pits:
                can_cross = False
                for ladder_base, ladder_top in ladders:
                    if ladder_base < snake_pit_start and ladder_top > snake_pit_end:
                        print(
                            f"Can cross snake-pit ({snake_pit_start}, {snake_pit_end}) with ladder ({ladder_base},{ladder_top})"
                        )
                        can_cross = True
                        break
                if not can_cross:
                    print(
                        f"Cannot cross snake-pit ({snake_pit_start}, {snake_pit_end})"
                    )
                    return True
        return False

    if has_no_path():
        return -1

    @profile
    def create_edge_lists() -> list[list[int]]:
        ret = [[] for _ in range(n)]
        for pos in range(n):
            l = ret[pos]
            for move_size in range(1, DICE_SIZE + 1):
                new_pos = pos + move_size
                if new_pos > last:
                    continue  # too far, let's ignore this move.
                teleported_new_pos = new_pos
                if moves[new_pos] != -1:
                    teleported_new_pos = moves[new_pos]
                l.append(teleported_new_pos)
        return ret

    # iterative dfs - runs into recursion limit
    @profile
    def min_rolls_from(pos: int) -> int:
        visiting = set()
        # visiting = []
        stack = [(pos, False)]
        num_rolls = 0
        min_num_rolls = 1000000000
        min_path = set()
        # min_path = []
        edge_lists = create_edge_lists()
        print(f"num_edges={sum([len(edge_list) for edge_list in edge_lists])//2}")
        num_paths_abandoned = 0
        while stack:
            pos, is_backtracking = stack.pop()
            # print(f"{'..'*num_rolls}Removed from stack: {pos}")
            if is_backtracking:
                visiting.remove(pos)
                num_rolls = num_rolls - 1
                # print(f"{'..'*num_rolls}Backtracked from {pos}. Decremented num_rolls down to {num_rolls}: Path so far = {visiting} in unknown order")
                # print(f"{'..'*num_rolls}Backtracked from {pos}. Decremented num_rolls down to {num_rolls}: Path so far = {visiting}")
                continue
            if pos in visiting:
                # detected cycle
                # print(f"found cycle at {pos}, abandoning this branch")
                continue
            if pos == last:
                # reached the last cell.
                if num_rolls < min_num_rolls:
                    min_num_rolls = num_rolls
                    min_path = visiting | {pos}
                    # min_path = (visiting + [pos])
                    print(
                        f"{'..'*num_rolls}Reached the end through {min_path} in unknown order. Updated min_num_rolls to {min_num_rolls}"
                        # f"{'..'*num_rolls}Reached the end through {min_path}. Updated min_num_rolls to {min_num_rolls}"
                    )
                else:
                    print(
                        f"{'..'*num_rolls}Reached the end through {min_path} in some unknown order in {min_num_rolls} rolls, which fails to update min_num_rolls={min_num_rolls}"
                    )
                    # print(f"{'..'*num_rolls}Reached the end through {min_path} in {min_num_rolls} rolls, which fails to update min_num_rolls={min_num_rolls}")
                    ...
                continue
            if num_rolls >= min_num_rolls - 2:
                num_paths_abandoned += 1
                # print(
                #     f"{'..'*num_rolls}abandoning visiting {visiting|{pos}} because this path won't more efficient than the most efficient known path"
                # )
                # print(f"{'..'*num_rolls}abandoning visiting {visiting+[pos]} because this path won't more efficient than the most efficient known path")
                continue
            visiting.add(pos)
            # visiting.append(pos)
            num_rolls = num_rolls + 1
            # print(f"{'..'*num_rolls}Visited {pos}. Incremented num_rolls to {num_rolls}: Path so far = {visiting} in unknown order")
            # print(f"{'..'*num_rolls}Visited {pos}. Incremented num_rolls to {num_rolls}: Path so far = {visiting}")
            stack.append((pos, True))
            next_node_candidates = []
            for teleported_nxt in edge_lists[pos]:
                if teleported_nxt not in visiting:
                    next_node_candidates.append(teleported_nxt)
            for teleported_nxt in sorted(next_node_candidates):
                # print(f"{'..'*num_rolls}Pushing to stack {teleported_nxt}")
                stack.append((teleported_nxt, False))
        print(
            f"min_num_rolls={min_num_rolls}, through path {min_path} in unknown order"
        )
        # print(f"min_num_rolls={min_num_rolls}, through path {min_path}")
        print(f"num_paths_abandoned={num_paths_abandoned}")
        return min_num_rolls

    return min_rolls_from(0)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        n = int(sys.argv[1])
        if len(sys.argv) - 2 != n:
            raise ValueError(
                f"Number of input arguments on the CLI isn't correct. Identified n = {n}. Expected {n} more arguments after n, but found {len(sys.argv)-2}"
            )
        moves = [
            int(arg[:-1]) if not arg[-1].isdigit() else int(arg) for arg in sys.argv[2:]
        ]
    else:
        test = test10
        n = test.n
        moves = test.moves
        expected_min_moves = test.expected_min_moves
    print(f"n={n}")
    if n < 100:
        print(f"moves={moves}")
    min_moves = minimum_number_of_rolls(n, moves)
    print(f"min_moves={min_moves},expected_min_moves={expected_min_moves}")
