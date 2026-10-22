def minmax(x, y):
    if x < y:
        return x, y
    else:
        return y, x

a = float(input())
b = float(input())
c = float(input())
d = float(input())

min_ab, max_ab = minmax(a, b)
min_abc, _ = minmax(min_ab, c)
_, max_abc = minmax(max_ab, c)
min_final, _ = minmax(min_abc, d)
_, max_final = minmax(max_abc, d)

print(min_final)
print(max_final)