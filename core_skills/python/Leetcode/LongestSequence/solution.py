    class Solution:
        def longest_consecutive(self, nums):
            if len(nums) == 0:
                return 0

            # Step 1: Remove duplicates and sort
            nums = sorted(set(nums))
            print("Sorted unique:", nums)

            # Step 2: Count consecutive elements
            max_length = 1
            curr_length = 1

            for i in range(1, len(nums)):
                if nums[i] == nums[i - 1] + 1:   # Consecutive?
                    curr_length += 1
                else:
                    curr_length = 1               # Reset

                max_length = max(max_length, curr_length)

            return max_length


    nums = [100, 4, 100, 1, 3, 2]
    a = Solution()
    print(a.longest_consecutive(nums))
