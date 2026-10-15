n = int(input())
s = []
for i in range(n):
    s.append(input())
letter = input()
print([x for x in s if x[0] == letter])