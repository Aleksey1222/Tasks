n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

target_v = int(input())
for key, value in d.items():
    if value == target_v:
        print(key)
        break
