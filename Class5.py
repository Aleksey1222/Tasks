class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

n = int(input())
points = []
for _ in range(n):
    x = int(input())
    y = int(input())
    points.append(Point(x, y))

best = max(points, key=lambda p: p.x)
print(best.x)
print(best.y)