####
# Soundex.py shall determine a words pronunciation according to the soundex method.
# Marcel Wagner

import sys

# Table for all 26 letters
table = {
   'B': 1,
   'F': 1,
   'P': 1,
   'V': 1,
   'C': 2,
   'G': 2,
   'J': 2,
   'K': 2,
   'Q': 2,
   'S': 2,
   'X': 2,
   'Z': 2,
   'D': 3,
   'T': 3,
   'L': 4,
   'M': 5,
   'N': 5,
   'R': 6,
   'A': 0,
   'E': 0,
   'I': 0,
   'O': 0,
   'U': 0,
   'W': 0,
   'Y': 0,
   'H': 0
}

# Determine word according to soundex method
def soundex(word):
   # Empty result list
   result = []
   # Make input uniform uppercase
   word = word.upper()
   # Loop over the length of the word
   for i in range(0,len(word)):
      # Push the first letter into the result list
      if 0 == i:
         result.append(word[i])
      # If the number from the table is not 0  or not the same value as the last character
      # Push the value from the table into the result string
      else:
         if 0 != table[word[i]]:
            if str(table[word[i]]) != result[len(result)-1]:
               result.append(str(table[word[i]]))
         else:
            pass
   # If the string is not long enough fill with 0's
   while len(result) < 6:
      result.append('0')
   # Join the result list into a string and return it
   return ''.join(result).lower()