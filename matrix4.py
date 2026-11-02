m, n = map(int, input().split())
a = [[j for j in range(n)] for _ in range(m)]
for row in a:
    print(*row)