class Solution:
    def check_duplicates(self, my_list):
        list_len = len(my_list)
        set_len = len(set(my_list))

        if list_len == set_len :
            return False
        
        else :
            return True

        print(list_len)
        print(set_len)

    def check_without_inbuilt(self, my_list):

        duplicate_flag = 0

        for i in my_list :
            if



nums = [1,2,3,4,5,6,7]

a= Solution()
print(a.check_duplicates(nums))
