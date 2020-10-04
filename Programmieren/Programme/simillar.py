import soundex
import sys


file = open('words.txt')
lines = file.readlines()

result = []
valid_lines = []
for line in lines:
   if(all(65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122 for ch in line.strip())):
      valid_lines.append(line.strip())


# valid_lines = valid_lines[0:100]
# print (valid_lines)

for line in valid_lines:
   result.append((line, soundex.soundex(line)))

compare = (sys.argv[1],soundex.soundex(sys.argv[1]))
print(compare)

print(list(x for x in result if x[1] == compare[1]))