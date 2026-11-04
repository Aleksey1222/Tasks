class Counter:
    def __init__(self):
        self.total = 0

    def inc(self):
        self.total += 1

    def dec(self):
        self.total -= 1

    def value(self):
        return self.total

c = Counter()
for _ in range(3):
    cmd = input()
    if cmd == "inc":
        c.inc()
    elif cmd == "dec":
        c.dec()
    else:
        print(c.value())