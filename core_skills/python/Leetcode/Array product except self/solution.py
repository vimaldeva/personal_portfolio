    class Solution:
        def product_except_self(self, nums):

            n = len(nums)

            # Step 1: Build prefix array
            prefix = [1] * n
            for i in range(1, n):
                prefix[i] = prefix[i - 1] * nums[i - 1]

            print("Prefix:", prefix)

            # Step 2: Build suffix array
            suffix = [1] * n
            for i in range(n - 2, -1, -1):
                suffix[i] = suffix[i + 1] * nums[i + 1]

            print("Suffix:", suffix)

            # Step 3: Multiply prefix and suffix
            answer = [1] * n
            for i in range(n):
                answer[i] = prefix[i] * suffix[i]

            print("Answer:", answer)
            return answer


    # Test Case 1
    nums = [1, 2, 3, 4]
    sol = Solution()
    sol.product_except_self(nums)
