class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, name, qty):
        self.items[name] = self.items.get(name, 0) + qty

    def total(self):
        return sum(self.items.values())

inv = Inventory()
for _ in range(3):
    name = input()
    qty = int(input())
    inv.add(name, qty)

print(inv.total())