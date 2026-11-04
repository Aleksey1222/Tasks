class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

x = int(input())
y = int(input())
p = Point(x, y)
print(p.x)
print(p.y)