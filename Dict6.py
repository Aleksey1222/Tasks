n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

total = 0
for value in d.values():
    total += value
print(total)
