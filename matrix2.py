m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]
for j in range(n):
    for i in range(m):
        print(a[i][j], end=' ')
    print()