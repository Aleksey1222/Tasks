n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

for value in d.values():
    print(value)
