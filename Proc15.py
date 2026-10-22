def shift_left3(a, b, c):
    return b, c, a

a1 = float(input())
b1 = float(input())
c1 = float(input())
a2 = float(input())
b2 = float(input())
c2 = float(input())

r1, r2, r3 = shift_left3(a1, b1, c1)
print(r1)
print(r2)
print(r3)

r1, r2, r3 = shift_left3(a2, b2, c2)
print(r1)
print(r2)
print(r3)