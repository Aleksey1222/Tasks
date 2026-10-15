n = int(input())
a = []
for i in range(n):
    a.append(input())
print(sorted(a, key=len))
print(max(a, key=len))