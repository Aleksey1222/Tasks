def is_square(k):
    if k < 0: return False
    root = int(k ** 0.5)
    return root * root == k

for _ in range(10):
    k = int(input())
    print(is_square(k))
