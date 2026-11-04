class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

x = int(input())
y = int(input())
p = Point(x, y)
print(p)              # один print — формуляр через __str__