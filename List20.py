n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
pos = [x for x in a if x > 0]
print(pos)
print(len(pos))