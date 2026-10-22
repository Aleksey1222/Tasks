def rect_ps(x1, y1, x2, y2):
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    p = 2 * (width + height)
    s = width * height
    return p, s

for _ in range(3):
    x1 = float(input())
    y1 = float(input())
    x2 = float(input())
    y2 = float(input())
    p, s = rect_ps(x1, y1, x2, y2)
    print(p)
    print(s)