class Solution:
    def group_anagram(self, ana_list):
        temp_dict = dict()

        for i in range(len(ana_list)):
            # Clean the word
            cleaned = ana_list[i].replace(' ', '')
            cleaned = ''.join(a for a in cleaned if a.isalpha())

            # Create sorted key
            sorted_word = ''.join(sorted(cleaned))

            # Group: sorted_word → [original words]
            if sorted_word in temp_dict:
                temp_dict[sorted_word].append(ana_list[i])
            else:
                temp_dict[sorted_word] = [ana_list[i]]

        # Extract grouped lists
        grouped_ana = list(temp_dict.values())
        print(grouped_ana)
        # print(temp_dict)
        return grouped_ana


test_ana = ["eat", "tea", "tan", "ate", "nat", "bat"]
a = Solution()
a.group_anagram(test_ana)
