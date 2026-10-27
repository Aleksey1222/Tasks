n = int(input())
d1 = {}
for _ in range(n):
    key = input()
    value = int(input())
    d1[key] = value

m = int(input())
d2 = {}
for _ in range(m):
    key = input()
    value = int(input())
    d2[key] = value

d1.update(d2)
for key, value in d1.items():
    print(f"{key}: {value}")
