
class Solution:

    def is_anagram(self, word1, word2):
        str1 = word1.lower()
        str2 = word2.lower()

        str1 = str1.replace(' ','')
        str2 = str2.replace(' ','')

        # Remove everything that is NOT a letter
        str1 = ''.join(c for c in str1 if c.isalpha())
        str2 = ''.join(c for c in str2 if c.isalpha())
        
        hash_map = [0] * 26

        for i in word1 :
            hash_map[ord(i) - ord('a')] += 1
        for i in word2 :
            hash_map[ord(i) - ord('a')] -= 1   

        final_sum = 0
        for count in hash_map :
            if count != None :
                final_sum += count  

        for count in hash_map:
            if count != 0:                      # ✅ Check EACH count
                return False
        return True


word1 = 'testing'
word2 = 'sitting'  

a = Solution()
print(a.is_anagram(word1,word2))
