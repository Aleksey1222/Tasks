m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]

total = sum(sum(row) for row in a)
mx = max(max(row) for row in a)
print("sum =", total)
print("max =", mx)