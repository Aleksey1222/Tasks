n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

for key in list(d):
    if d[key] % 2 == 0:
        del d[key]

for key, value in d.items():
    print(f"{key}: {value}")
