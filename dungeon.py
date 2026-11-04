import random

prices = {"зелье": 10, "факельное_масло": 15, "боевой_эликсир": 40}

enemy_stats = {
    "скелет":        {"hp": 45, "damage": 6, "loot": 25},
    "упырь":         {"hp": 30, "damage": 4, "loot": 15},
    "паук":          {"hp": 20, "damage": 3, "loot": 10},
    "летучая_мышь":  {"hp": 12, "damage": 2, "loot": 5},
}

class Hero:
    def __init__(self, name, health, strength, agility, endurance):
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        
        self.damage = 10 + strength * 1.5
        self.crit_damage = self.damage * 2
        self.stamina = health // 10 + endurance

    def __str__(self):
        return f"{self.name}: здоровье {self.health}, урон {self.damage:.1f}, стамина {self.stamina}"

    def strike(self, n):
        if n % 3 == 0:
            return self.crit_damage, True
        return self.damage, False

    def spend_stamina(self, cost):
        if self.stamina >= cost:
            self.stamina -= cost
            return False
        self.health -= cost - self.stamina
        self.stamina = 0
        return True

    def heal(self, amount, cap):
        self.health = min(self.health + amount, cap)

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "stamina": self.stamina,
            "strength": self.strength,
            "agility": self.agility,
            "endurance": self.endurance
        }

    @staticmethod
    def from_dict(data):
        hero = Hero(
            data["name"],
            data["health"],
            data["strength"],
            data["agility"],
            data["endurance"]
        )
        hero.stamina = data["stamina"]
        return hero

class Enemy:
    def __init__(self, name, stats):
        self.name = name
        self.hp = float(stats["hp"])
        self.damage = stats["damage"]
        self.loot = stats["loot"]

def fight(enemy, hero, bonus=0):
    rounds = []
    round_n = 0
    print(f"Вы спускаетесь по лестнице. Из темноты появляется {enemy.name}!")
    
    while enemy.hp > 0 and hero.health > 0:
        round_n += 1
        hit, crit = hero.strike(round_n)
        hit += bonus
        enemy.hp -= hit
        line = f"Раунд {round_n}: герой наносит {hit:.1f}"
        if crit:
            line += " - КРИТИЧЕСКИЙ УДАР!"
            
        if enemy.hp <= 0:
            line += " Враг повержен."
            rounds.append([round_n, hit, 0])
        else:
            blow = enemy.damage
            hero.health -= blow
            line += f" Здоровье {enemy.name}: {enemy.hp:.1f}. {enemy.name.capitalize()} бьет на {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
        
    won = enemy.hp <= 0
    loot = enemy.loot if won else 0
        
    return rounds, won, loot

def buy(price, gold, quantity=1):
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False