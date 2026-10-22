def sort_inc3(a, b, c):
    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a
    return a, b, c

a1 = float(input())
b1 = float(input())
c1 = float(input())

a2 = float(input())
b2 = float(input())
c2 = float(input())

v1, v2, v3 = sort_inc3(a1, b1, c1)
print(v1)
print(v2)
print(v3)

v1, v2, v3 = sort_inc3(a2, b2, c2)
print(v1)
print(v2)
print(v3)