# Aufgabenblatt 2 Aufgabe 3
# Plotten Sie die Punkte der Geradengleichungy= 0.5·x+1 zwischen 0 und 99. 
# Aber die Werte sollen um bis zu 17 zufällig nach oben schwanken.
# Lesen Sie die Dokumentation und zeichnen Sie eine Gerade ein, die der linearen Regression entspricht. 
# Sie kriegen sowohl die Werte der Geradengleichung als auch eine Funktion, die Ihnen die Werte berechnet.
# Author: Marcel Wagner
# Studiengang: Master Autonomes Fahren
# Datum: 23.10.2020


import matplotlib.pyplot as plt 
import numpy as np

np.random.seed(42)

x = np.arange(0, 99, 1)
random = np.random.random_sample(99) * 17
y = 0.5*x + 1 + random

m,b = np.polyfit(x,y,1)

plt.scatter(x,y)
plt.plot(x, m*x+b, 'r')
plt.title('Zufallswerte mit linerarer Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.text(50, m*50, 'y = '+str(np.round(m,2))+'x + '+str(np.round(b,2)), color='red')
plt.show()