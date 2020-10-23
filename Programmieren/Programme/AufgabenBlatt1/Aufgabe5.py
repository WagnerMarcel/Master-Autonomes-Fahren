lis = [1, 2, 3] 
for ele in lis: 
   print(ele)

idx = 0
while idx < len(lis):
   print(lis[idx])
   idx += 1


dic = {1: "eins", 2: "zwei", 3: "drei"} 
lis = list(dic.keys())
idx = 0
while idx < len(lis):
   key = lis[idx] 
   print(key, dic[key]) 
   idx = idx + 1

for ele in lis:
   print(ele, dic[ele])

