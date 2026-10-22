import math

def triangle_ps(a):
    p = 3 * a
    s = (a**2 * math.sqrt(3)) / 4
    return p, s

for _ in range(3):
    a = float(input())
    p, s = triangle_ps(a)
    print(p)
    print(s)