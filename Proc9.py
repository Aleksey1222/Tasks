def add_left_digit(d, k):
    count = 0
    temp = k
    while temp > 0:
        count += 1
        temp //= 10
    return d * (10 ** count) + k

k = int(input())
d1 = int(input())
d2 = int(input())

step1 = add_left_digit(d1, k)
print(step1)

step2 = add_left_digit(d2, step1)
print(step2)