class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        i = 0
        result = 0
        while i< len(nums):
            result ^= nums[i] 
            print(f'result: {result} ^ nums[i]: {nums[i]}')
            i += 1
        return result


p1 = Solution()
print(f"singleNumber: {p1.singleNumber([4,6,3,9,5,6,3,4,5])}")
