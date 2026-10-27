def triangle_p(a, h):
    side = ((a / 2) ** 2 + h ** 2) ** 0.5
    return a + 2 * side

for _ in range(3):
    a = float(input())
    h = float(input())
    print(triangle_p(a, h))
