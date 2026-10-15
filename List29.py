n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
k = int(input())
print(sorted(a, reverse=True)[:k])