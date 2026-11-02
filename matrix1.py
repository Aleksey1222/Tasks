m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]
for row in a:
    print(*row)