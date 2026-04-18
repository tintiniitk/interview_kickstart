class Solution:
    def maxSubarraySum(self, arr, k):
        # code here
        n = len(arr)
        max_sum = cur_sum = sum(arr[0:k])
        for i in range(1, n - k + 1):
            # cur_sum = sum(arr[i:k+i])
            cur_sum += arr[k + i - 1]
            cur_sum -= arr[i - 1]
            if cur_sum > max_sum:
                max_sum = cur_sum
        return max_sum


if __name__ == "__main__":
    arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
    k = 4
    s = Solution()
    print(f"max sum = {s.maxSubarraySum(arr,k)}")
