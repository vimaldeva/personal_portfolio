class Solution :
    def top_k_frequency(self, my_list, k) :

        hash_dict = dict()
        for i in range(0, len(my_list)):
            if my_list[i] in hash_dict :
                hash_dict[my_list[i]] += 1
            else :
                hash_dict[my_list[i]] = 1

        print(hash_dict)

        freq_list = []

        for num, count in hash_dict.items():
            freq_list.append([count, num])
        
        print("before sorte :  ",freq_list)

        sorted_list = sorted(freq_list, reverse= True)

        print("sorted list :  ",sorted_list)

        result = []
        for i in range(k):
            result.append(freq_list[i][1])  # [1] = the number

        print("Top K:", result)
        return result






nums = [2,2,2,5,5,7]
k= 2
a = Solution()

a.top_k_frequency(nums,3)
