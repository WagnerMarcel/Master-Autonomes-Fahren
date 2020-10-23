# Aufgabenblatt 2 Aufgabe 1
# Verschiedene numpy operationen auf einem 1000x1000 Array mit einer Millionen Zufallszahlen.
# Author: Marcel Wagner
# Studiengang: Master Autonomes Fahren
# Datum: 23.10.2020

import numpy as np

np.random.seed(42)
a = np.random.random_sample(10**6).reshape((10**3, 10**3))

print('Linkes oberes element: '+  str(a[0][0]))
print('Maximum: ' + str(np.max(a)))
print('Minimum: ' + str(np.min(a)))
print('Durchschnitt: ' + str(np.average(a)))
print('Summe: ' + str(np.sum(a)))
print('Diagonale links oben nach rechts unten: ' + str(np.sum(np.diag(a))))
print('Diagonale rechts oben nach links unten: ' + str(np.sum(np.fliplr(a).diagonal())))
print('Anzahl der Zahlen groesser als der Durchschnitt: ' + str(np.count_nonzero(a > np.average(a))))
print('Anzahl der Zeilen mit einem Mittel groesser als der Durchschnitt: ' + str(np.count_nonzero(np.average(a, axis=1) > np.average(np.average(a, axis=1)))))
print('Anzahl der Spalten mit einem Mittel groesser als der Durchschnitt: ' + str(np.count_nonzero(np.average(a, axis=0) > np.average(np.average(a, axis=1)))))
b = np.where(a > np.average(a), 1,0)
print('Binarisiertes Array, Anzahl der nullen: ' + str(np.sum(np.size(b))-np.count_nonzero(b)))