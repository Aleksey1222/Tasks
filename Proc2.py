def power_a234(a):
    return a**2, a**3, a**4

for _ in range(5):
    a = float(input())
    p2, p3, p4 = power_a234(a)
    print(p2)
    print(p3)
    print(p4)