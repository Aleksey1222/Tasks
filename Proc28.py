def digit_count(k):
    k = abs(k)
    if k < 10:
        return 1
    return 1 + digit_count(k // 10)

for _ in range(5):
    k = int(input())
    print(digit_count(k))
