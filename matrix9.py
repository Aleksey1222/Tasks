m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]

row_sums = [sum(row) for row in a]
col_sums = [sum(a[i][j] for i in range(m)) for j in range(n)]

print("строки:", row_sums)
print("столбцы:", col_sums)