class Hero:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "damage": self.damage,
        }

    @staticmethod
    def from_dict(data):
        return Hero(data["name"], data["health"], data["damage"])

name = input()
health = int(input())
damage = int(input())

hero = Hero(name, health, damage)
data = hero.to_dict()
new_hero = Hero.from_dict(data)   # вызываем именем класса
print(new_hero.health)