n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
s = 0
for i in range(1, len(a), 2):
    print(a[i])
    s = s + a[i]
print(s)