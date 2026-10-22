def add_right_digit(d, k):
    return k * 10 + d

k = int(input())
d1 = int(input())
d2 = int(input())

step1 = add_right_digit(d1, k)
print(step1)

step2 = add_right_digit(d2, step1)
print(step2)