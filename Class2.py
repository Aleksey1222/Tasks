class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def shift(self, dx, dy):
        self.x += dx
        self.y += dy

x = int(input())
y = int(input())
dx = int(input())
dy = int(input())

p = Point(x, y)
p.shift(dx, dy)      # метод меняет состояние, возвращает None — без присваивания
print(p.x)
print(p.y)