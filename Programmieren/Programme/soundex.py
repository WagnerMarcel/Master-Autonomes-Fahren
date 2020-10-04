import sys

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

def soundex(word):
   result = []
   word = word.upper()
   for i in range(0,len(word)):
      if 0 == i:
         result.append(word[i])
      else:
         if 0 != table[word[i]]:
            if str(table[word[i]]) != result[len(result)-1]:
               result.append(str(table[word[i]]))
         else:
            pass
   while len(result) < 6:
      result.append('0')
   return ''.join(result).lower()


# for i in range(1, len(sys.argv)):
#    print(sys.argv[i], ' : ', soundex(sys.argv[i]))
   