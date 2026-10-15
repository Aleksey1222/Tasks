n = int(input())
s = []
for i in range(n):
    s.append(input())
print([len(x) for x in s])
print(sum(len(x) for x in s))