import sys


def helper(n: int, src: int, dst: int, inm: int, ret: list[int]):
    if n == 0:
        return
    if n == 1:
        ret.append([src, dst])
        return
    helper(n-1,src,inm,dst,ret)
    helper(1,src,dst,inm,ret)
    helper(n-1,inm,dst,src,ret)


def tower_of_hanoi(n) -> list[list[int]]:
    """
    Args:
     n(int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    ret=[]
    helper(n,1,3,2,ret)
    return ret


if __name__ == "__main__":
	n = 8
	if len(sys.argv) > 1:
		n = int(sys.argv[1])
	tower = tower_of_hanoi(n)
	print(f"steps for tower for hanoii for n={n} => {len(tower)} steps => {tower}")
