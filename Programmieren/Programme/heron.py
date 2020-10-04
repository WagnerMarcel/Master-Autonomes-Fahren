import sys
import math

def heron(x = 10, epsilon = 10**-6):
   #Calculate the square root of a given number up to a given last digit.
   a = 0
   a_new = 1 + x / 2
   count = 0
   iterations = [a_new]
   while abs(a_new - a) >= epsilon:
      a = a_new
      a_new = (a + (x/a))/2
      count += 1
      iterations.append(a_new)

   print('Correct Value: ', math.sqrt(x))
   print('Calculated Value: ', a_new)
   print('Used Iterations: ', count)
   print('All iterations: ', iterations)

if len(sys.argv) <= 1:
   heron()
elif len(sys.argv) == 2:
   heron(float(sys.argv[1]))
else:
   heron(float(sys.argv[1]), float(sys.argv[2]))

