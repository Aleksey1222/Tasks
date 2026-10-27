def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

count = 0
for _ in range(10):
    n = int(input())
    if is_prime(n):
        count += 1
print(count)
