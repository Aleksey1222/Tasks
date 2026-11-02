m, n = map(int, input().split())
a = [[i for _ in range(n)] for i in range(m)]
for row in a:
    print(*row)