def digit_sum(k):
    k = abs(k)
    if k == 0:
        return 0
    return (k % 10) + digit_sum(k // 10)

for _ in range(5):
    k = int(input())
    print(digit_sum(k))
