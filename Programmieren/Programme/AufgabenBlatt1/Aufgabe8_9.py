# Primzahlen bis 100
print(list(x for x in range(100) if 0 not in [x%y for y in range(2,x)]))

# Geradzahlige Quadratzahlen
print(list(x**3 for x in range(10) if x**3 % 2 == 0 ))

# Alle Teiler ausser 1 und z (testen Sie mit 123, 12345, 123456)
z = 12345
print(list(x for x in range(2,z) if (z / x)%1 == 0 ))

#Alle Primzahlen zwischen 10000 und 10100
print(list(x for x in range(10000, 10100) if 0 not in [x%y for y in range(2,x)]))

# Kleinste zahl aus der Summe zweier kubikzahlen
size = 12
result = list(x for x in list(((x,y),(p,q)) for x in range(1,size+1) for y in range(1,size+1) for p in range(1,size+1) for q in range(1,size+1))
      if (x[0][0]**3 + x[0][1]**3 == x[1][0]**3 + x[1][1]**3) 
         & (
            (x[0][0] != x[0][1]) &
            (x[0][0] != x[1][0]) &
            (x[0][0] != x[1][1]) &
            (x[0][1] != x[1][0]) &
            (x[0][1] != x[1][1]) 
         ))

print(result)
finalResult = []
finalResult.append(result[0])
for i in result:
   for j in finalResult:
      if ((i[0][0] != j[0][0]) & (i[0][0] != j[0][1]) & (i[0][0] != j[1][0]) & (i[0][0] != j[1][1]) & 
         (i[0][1] != j[0][0]) & (i[0][1] != j[0][1]) & (i[0][1] != j[1][0]) & (i[0][1] != j[1][1]) &
         (i[1][0] != j[0][0]) & (i[1][0] != j[0][1]) & (i[1][0] != j[1][0]) & (i[1][0] != j[1][1]) &
         (i[1][1] != j[0][0]) & (i[1][1] != j[0][1]) & (i[1][1] != j[1][0]) & (i[1][1] != j[1][1])):
         print(i)
         
print(finalResult)