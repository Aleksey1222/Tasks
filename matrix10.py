m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]

t = [[a[i][j] for i in range(m)] for j in range(n)]
for row in t:
    print(*row)