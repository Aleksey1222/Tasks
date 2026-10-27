def circle_area(r):
    return 3.14159 * (r ** 2)

def ring_s(r1, r2):
    return circle_area(r1) - circle_area(r2)

for _ in range(3):
    r1 = float(input())
    r2 = float(input())
    print(ring_s(r1, r2))
