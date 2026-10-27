n = int(input())
d = {}
for _ in range(n):
    key = input()
    value = int(input())
    d[key] = value

inverted = {}
for key, value in d.items():
    inverted[value] = key

for key, value in inverted.items():
    print(f"{key}: {value}")
