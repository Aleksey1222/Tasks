n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
total = 0
product = 1
for i in range(len(a)):
    total = total + a[i]
    if i % 2 == 0:
        product = product * a[i]
print(total)
print(product)