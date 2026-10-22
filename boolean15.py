# Boolean15. Проверить, ровно два из A, B, C положительные.
a = int(input())
b = int(input())
c = int(input())
count = (a > 0) + (b > 0) + (c > 0)
print(count == 2)
