n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

for name, price in d.items():
    print(f"{name}: {price}")
