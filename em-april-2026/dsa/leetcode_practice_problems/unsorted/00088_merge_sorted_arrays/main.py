class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i1 = m - 1
        n1 = 0
        i2 = n - 1
        n2 = 0
        i = m + n - 1
        while i1 >= n1 and i2 >= n2:
            if nums1[i1] > nums2[i2]:
                nums1[i] = nums1[i1]
                i1 = i1 - 1
            else:
                nums1[i] = nums2[i2]
                i2 = i2 - 1
            i = i - 1
        while i1 >= n1:
            nums1[i] = nums1[i1]
            i1 = i1 - 1
            i = i - 1
        while i2 >= n2:
            nums1[i] = nums2[i2]
            i2 = i2 - 1
            i = i - 1
        return


if __name__ == "__main__":
    s = Solution()
    nums1 = [2, 432, 4325, 232432, 0, 0, 0]
    nums2 = [34, 356, 64364]
    s.merge(nums1, 4, nums2, 3)
    print(f"nums1 = {nums1}")
