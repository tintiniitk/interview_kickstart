TYPE_INVALID = -1
TYPE_START = 0
TYPE_END = 1
TYPE_LAND = 2
TYPE_WATER = 3
TYPE_DOOR = 4
TYPE_KEY = 5
types_str = ['start','end','land','water','door','key']

from typing import NamedTuple
from collections import deque

class Visited(NamedTuple):
    yes: bool = False
    keys: set[int] = set()

class BFSQueueEntry(NamedTuple):
    node: int = -1
    keys: set[int] = set()
    path: list[int] = []

def key_or_door(cell_value: str) -> tuple[int, int]:
    """ returns TYPE_KEY if key else TYPE_DOOR, index of lock/key (0-9) . """
    ord_of_cell_value = ord(cell_value)
    if ord_of_cell_value >= ord("A") and ord_of_cell_value <= ord("J"):
        return TYPE_DOOR, ord_of_cell_value - ord("A")
    if ord_of_cell_value >= ord("a") and ord_of_cell_value <= ord("j"):
        return TYPE_KEY, ord_of_cell_value - ord("a")
    raise ValueError(f"Cell value {cell_value} is not a valid key/door value")

def type_of_cell(cell_value: str) -> tuple[int, int]:
    match cell_value:
        case '@':
            return TYPE_START, -1
        case '+':
            return TYPE_END, -1
        case '.':
            return TYPE_LAND, -1
        case '#':
            return TYPE_WATER, -1
    return key_or_door(cell_value)

def find_shortest_path(grid):
    """
    Args:
     grid(list_str)
    Returns:
     list_list_int32
    """
    # Write your code here.
    # grid is an array of str
    if not grid:
        return []

    # primary derivative data
    rows = len(grid)
    cols = len(grid[0])
    num_cells = rows * cols
    n = num_cells

    # assuming each row has len = cols
    nbr_offsets = [-1,1,-cols,cols]

    # secondary derivative data
    types = [TYPE_INVALID for _ in range(n)]
    doors_and_keys = [-1 for _ in range(n)]
    start_cell_index = -1
    end_cell_index = -1
    index = 0
    for i in range(rows):
        row = grid[i]
        for j in range(cols):
            cell_type, door_index = type_of_cell(row[j])
            types[index] = cell_type
            match cell_type:
                case x if x == TYPE_DOOR:
                    doors_and_keys[index] = door_index
                case x if x == TYPE_KEY:
                    doors_and_keys[index] = door_index
                case x if x == TYPE_START:
                    start_cell_index = index
                case x if x == TYPE_END:
                    end_cell_index = index
            index += 1
    # print(f"{[types_str[cell_type] for cell_type in types]}")
    # edge-case
    if start_cell_index == end_cell_index:
        return [start_cell_index]
    if start_cell_index < 0 or start_cell_index >= n:
        raise ValueError(f"No start-cell found in the grid")
    if end_cell_index < 0 or end_cell_index >= n:
        raise ValueError(f"No end-cell found in the grid")
    # print(f"doors_and_keys={doors_and_keys}")
    # print(f"start_cell_index={start_cell_index},end_cell_index={end_cell_index}")

    def get_valid_nxt_nodes(node: int) -> list[int]:
        valid_nxt_nodes = []
        col_num = node % cols
        if (col_num != 0) and node > 0: # leftmost cell has no left neighbor
            valid_nxt_nodes.append(node - 1)
        if (col_num != (cols - 1)) and node < (n-1): # rightmost cell has no right neighbor
            valid_nxt_nodes.append(node + 1)
        if (node - cols) >= 0: # top neighbor
            valid_nxt_nodes.append(node - cols)
        if (node + cols) < n: # top neighbor
            valid_nxt_nodes.append(node + cols)
        return list(filter(lambda node: types[node] != TYPE_WATER, valid_nxt_nodes))

    # find paths - using BFS
    visited = [Visited() for _ in range(n)]
    min_path_len = 2e9
    min_path = []
    q = deque([BFSQueueEntry(node=start_cell_index)])
    while q:
        node, keys_so_far_orig, current_path_orig = q.popleft()
        keys_so_far = keys_so_far_orig.copy() # create a copy to avoid modifying the existing entry.
        current_path = current_path_orig.copy() # create a copy to avoid modifying the existing entry.
        # indentation='  '*len(current_path)
        # print(f"{indentation}Exploring {str([[cell//cols,cell%cols] for cell in current_path]):<40} -> {str([node//cols,node%cols]):<6}")
        # print(f"{indentation}  .. with keys={keys_so_far_orig}")
        if node == end_cell_index:
            new_potential_min_path_length = len(current_path) + 1
            # prefix = f"Reached end-node, "
            if new_potential_min_path_length < min_path_len:
                min_path_len = new_potential_min_path_length
                min_path = current_path + [end_cell_index]
                # print(f"{indentation}  {prefix}and updated min_path to {str([[cell//cols,cell%cols] for cell in min_path]):<40}")
            else:
                # print(f"{indentation}  {prefix}but failed to update existing min_path {str([[cell//cols,cell%cols] for cell in min_path]):<40}")
                ...
            continue
        if len(current_path) + 2 >= min_path_len: # there are minimum 2 more nodes to be added current_path i.e. node, end-node
        # and if they are not going to improve over the existing known min_path_len, then
        # it's pointless proceed down this path.
            # print(f"{indentation}  this path is already too expensive, so skipping it ...")
            continue
        # no need to check explicitly of water cell as it's been ignored while defining next nodes
        # skip if we are at a door to which we don't have key
        if types[node] == TYPE_DOOR and doors_and_keys[node] not in keys_so_far:
            # we need to turn back from this path
            # print(f"{indentation}  node {[node//cols,node%cols]} is door number {doors_and_keys[node]} for which we haven't found key yet")
            continue
        has_been_visited, keys_on_last_visit = visited[node]
        if has_been_visited and len(keys_so_far - keys_on_last_visit) == 0:
            # do not revisit the same node unless this time you have a key which you didn't have last time.
            # print(f"{indentation}  node {[node//cols,node%cols]} was already visited with same or more keys, so skipping.")
            continue
        visited[node] = Visited(True, keys_so_far)
        # print(f"{indentation}  Updated visited for {[node//cols,node%cols]} to {visited[node]} for keys_so_far={keys_so_far}")
        if types[node] == TYPE_KEY:
            keys_so_far.add(doors_and_keys[node])
            # print(f"{indentation}  keys updated to {keys_so_far}")
        # visiting[node] = True
        current_path = current_path + [node]
        valid_nxt_nodes = get_valid_nxt_nodes(node)
        for nxt_node in valid_nxt_nodes:
            q.append(BFSQueueEntry(node=nxt_node, keys=keys_so_far, path=current_path))
            # print(f"{indentation}  inserted {[nxt_node//cols,nxt_node%cols]} into q")
    return [[node // cols, node % cols] for node in min_path]


def main():
    grid=["+B...", "####.", "##b#.", "a...A", "##@##"]
    # grid = [".dj##.f.j#efejj..@e#+G.c.", ".hdI#.#aAghficDe#J.CGa.ba"]
    # grid=[".bddfCeCAeaEF.##I#Ga.#.e..#J..jDg#.", "CfbAjeje.#IJde#da#hH##.fhCa#.j#cAgg", "hJhb#.jDcgdC#i.JJBc##Had..b#.jd..bi", "a..iAcch.gfhGJaD.#fIdb#h#I.eaA#AeHf", "G.b.H.aI..fH#FcF#hh.Ci.i.#d..E..#.f", "#E#Da##Hhc#....#BDjBg.fgD.hgJe#ffja", "EabgD#B#GAbhcaF.dBBghaC#.D.B.#.f.A#", "ia.ADf.hCi.e.##.....g#hdb#j#JH.Ehgj", "fiGEJgIdfE.#H.##.a.+.d.ggegb#.#.IaI", "HaejJfhC.EHija#.dG#JcE.#fdgGei#ej.#", "b..gAf#.Ejg.hg.ebf#.f#JcgGah##.#..#", "d.a@fffG#b.IE##..j.fJhF..hf.J.gGHA.", "#hhHE.gci#b#hgAHd.Gf#d..ACb##E#DejD", "C.h.ABiah.iDB.#.#Ae.Bdd.j#igdh##hdg", ".ebb.gh#.dCeh#.g#ih##HI.#..fa.d.Ba.", "#...#h#.Hda.EG.b.fhb.Iah.#ee.Ieei..", ".#D##ieD#..Eff.cgi.fcaf.HaD#f#ddg#d", "#dcg#ad#bj###F#h##..cE#b#fA.i#F#AF.", "jDh#eGhIAIie.gDb.b..ffg#.E#D#hhc.dj", "Bhg.fibghF.e.ic##.jc#f#a#B#.ediFa..", "B##dBb.J#g#.##jG.BaG..A#.G#cbaGgadi", "ea.AbiafH#cba#g#h.#g.iHHjj#.da...cA", ".#dcA#hGJBFg.###jGe.i#.cfcG###..Dg.", "#fg.IgjgCCi#BDfieAIcAc#.CH.Jf.h.c..", "bf.GF##d.#C#.egch.hf#jf#dfjfeJ.g###", ".IGe#.H#C.gFjd.dBe#.##h.#D...ib.aah", ".a##ghgg.....defc##e.JEeJf..bbff#JB", "b.B.hG.Jg.a#.#a#D.b#da.d#je.ii#..FH", "a#iHeB#c##dJghh#.h#.#Ei#.aF#.f#.#.j", "f.eh#JB#.ag.j.fbh#.j#J#I#jfJE#.G.#d", "##C#d..e#G#hhb.#JdGcGHjg.#eC.G.fA.a", ".#Icb.fgJ..#F#.#bDAch#.Bj.aFFa.I#e.", "eI..Ebahcbc##h.C#gd..ehgfa.#A#g#..j", "dgi#ggc##.#G.jJi#egc.#e#e##ejB#fe#b", "J#GA#I.c.##g.#.ehbjj#jCEC.fd.##h.ij"]
    shortest_path=find_shortest_path(grid)
    print(f"len(shortest_path)={len(shortest_path)},shortest_path={shortest_path}")


if __name__ == "__main__":
    main()
