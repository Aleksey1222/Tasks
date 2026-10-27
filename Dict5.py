n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

k = input()
print(d.pop(k, 0))
