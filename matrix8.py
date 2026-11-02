m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]

rot = [[a[m - 1 - i][j] for i in range(m)] for j in range(n)]
for row in rot:
    print(*row)