n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

for key, value in d.items():
    if value > 50:
        print(key)
