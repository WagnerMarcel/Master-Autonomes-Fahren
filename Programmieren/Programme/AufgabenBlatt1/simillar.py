####
# Simillar.py shall find based on a given input value and a given dictionary 
# words that sound simillar according to the soundex method.
# Marcel Wagner

import soundex
import sys

# Get the input, and assume default values if not given
inputWord = sys.argv[1] if len(sys.argv) > 1 else 'Test'
inputFile = sys.argv[2] if len(sys.argv) > 2 else 'words.txt'

# Read the dictionary
file = open(inputFile)
lines = file.readlines()

# Result list of the dictionary converted to soundex values
result = []
# Lines of the dictionary which are in only ASCII
validLines = []
# Find valid lines which are in only ASCII
for line in lines:
   if(all(65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122 for ch in line.strip())):
      validLines.append(line.strip())

# Process the valid lines with the soundex method
for line in validLines:
   result.append((line, soundex.soundex(line)))

# Print the input
print((inputWord,soundex.soundex(inputWord)))
# Print the matched words from the dictionary
print(list(x for x in result if x[1] == compare[1]))