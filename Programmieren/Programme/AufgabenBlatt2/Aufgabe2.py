# Aufgabenblatt 2 Aufgabe 2
# Lesen Sie die Wörter der Datei words ein und plotten Sie je Länge die Anzahl der Wörter dieser Länge in einem Bar-Chart. 
# Beschriften Sie das Chart passend und zeigen Sie auf der häufigstenLänge die Anzahl der Vorkommen in Prozent an.
# Author: Marcel Wagner
# Studiengang: Master Autonomes Fahren
# Datum: 23.10.2020

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

file = open('words.txt', 'r', encoding='utf8', errors="ignore")

input = file.readlines()
lengths = np.array(list(len(x)-1 for x in input))
aggregatedLengths = np.array(list(np.count_nonzero(lengths == y) for y in range(1,23)))

plt.bar(range(1,23), aggregatedLengths)
plt.title('Anzahl der Buchstaben je Wort im Englischen')
plt.xlabel('Anzahl der Buchstaben')
plt.ylabel('Anzahl der Worte')
xOfHighestBar = np.argmax(aggregatedLengths)
plt.text(xOfHighestBar, aggregatedLengths[xOfHighestBar], str(np.round(aggregatedLengths[xOfHighestBar]/np.sum(aggregatedLengths)*100, 1)) + '%')
plt.show()