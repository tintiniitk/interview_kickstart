# https://leetcode.com/problems/permutations-ii/

from collections import deque
import itertools


class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        if n < 1:
            return []
        if n < 2:
            return [nums]
        # nums.sort() # nums is now sorted - is it needed ?
        q = deque()
        q.append([nums[0]])
        # print(f"Initially q = {q}")
        for i in range(1, n):
            num = nums[i]
            # print(f"At i = {i}, num = {num}, q={q}")
            while len(q) > 0:
                arr = q.popleft()
                # print(f" Inside len(q)>0, dealing with arr={arr}")
                if len(arr) > i:
                    # Put this back
                    q.appendleft(arr)
                    # print(f"   At end of len(q)>0 having dealt with arr={arr}, q={q}")
                    break
                if len(arr) < i:
                    raise f"  Got: len(arr) < i at i={i}"
                # it's guranteed that len(arr) == i
                # make all extensions of arr by inserting num in it
                # make new arr by inserting num at the beginning of arr and insert into q
                new_arr = [num] + arr
                q.append(new_arr)
                # make new arr by inserting num in the middle of arr and insert into q
                for j in range(1, i):
                    if arr[j - 1] != num:
                        new_arr = arr[:j] + [num] + arr[j:]
                        q.append(new_arr)
                # make new arr by inserting num at the end of arr and insert into q
                if arr[-1] != num:
                    new_arr = arr + [num]
                    q.append(new_arr)
                # print(f"   At end of len(q)>0 having dealt with arr={arr}, q={q}")
            # print(f"After i={i}, q = {q}")
            # Uniquify the list at this point
            l = list(q)
            l.sort()
            q = deque(list(l for l, _ in itertools.groupby(l)))
            # print(f"After i={i}, after uniquifying q, q = {q}")
        # print(f"q = {q}")
        return list(q)


if __name__ == "__main__":
    nums = [1, 2, 1, 2]
    s = Solution()
    permutations = s.permuteUnique(nums)
    print(f"nums = {nums}, permutations={permutations}")
