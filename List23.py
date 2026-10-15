n = int(input())
s = []
for i in range(n):
    s.append(input())
print(sorted(s, key=len))
print(max(s, key=len))