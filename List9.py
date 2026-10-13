n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
s = 0
for x in a:
    s = s + x
avg = s / len(a)
count = 0
for x in a:
    if x > avg:
        print(x)
        count = count + 1
print(count)