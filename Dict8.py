n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

max_val = max(d.values())
print(max_val)
