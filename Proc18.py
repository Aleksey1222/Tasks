def circle_area(r):
    return 3.14159 * (r ** 2)

for _ in range(3):
    r = float(input())
    print(circle_area(r))
