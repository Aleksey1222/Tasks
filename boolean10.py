# Boolean10. Проверить, ровно одно из A и B нечётное.
a = int(input())
b = int(input())
count = (a % 2 != 0) + (b % 2 != 0)
print(count == 1)
