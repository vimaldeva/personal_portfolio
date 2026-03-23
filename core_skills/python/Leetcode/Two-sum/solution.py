
class Solution:
    def two_sum(self, my_list, target):

        hash_map = {}

        for i in range(len(my_list)):
            complement = target - my_list[i]
            if complement in hash_map :
                return [ hash_map[complement],i]
            hash_map[my_list[i]] = i

        return None
    
nums = [3,1,7,9,2,4]
target = 10

a= Solution()
print(a.two_sum(nums, target))


