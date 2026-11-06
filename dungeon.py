"""Правила подземелья: герой, враги, бой."""

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "goblin": {"hp": 35, "damage": 5, "loot": 15},
    "orc": {"hp": 60, "damage": 8, "loot": 40},
    "troll": {"hp": 80, "damage": 10, "loot": 60},
}


class Hero:
    """Герой: состояние и правила под одной крышей."""

    def __init__(self, name, health, strength, agility, endurance):
        """Собирает поля героя и вычисляемые характеристики."""
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        self.damage = 10 + strength * 1.5
        self.crit_damage = self.damage * 2
        self.stamina = health // 10 + endurance

    def __str__(self):
        """Строка представления героя для print(hero)."""
        return (f"{self.name}: health {self.health}, "
                f"damage {self.damage:.1f}, stamina {self.stamina}")

    def strike(self, n):
        """Удар номер n: возвращает (урон, крит ли)."""
        if n % 3 == 0:
            return self.crit_damage, True
        return self.damage, False

    def spend_stamina(self, cost):
        """Тратит выносливость; излишек списывает со здоровья."""
        if self.stamina >= cost:
            self.stamina -= cost
            return False
        self.health -= cost - self.stamina
        self.stamina = 0
        return True

    def heal(self, amount, cap):
        """Лечит, не превышая потолок cap."""
        self.health = min(self.health + amount, cap)

    def to_dict(self):
        """Словарь для сохранения: имя, состояние и характеристики."""
        return {"name": self.name, "health": self.health,
                "stamina": self.stamina, "strength": self.strength,
                "agility": self.agility, "endurance": self.endurance}

    @staticmethod
    def from_dict(data):
        """Фабричный метод: собирает героя из словаря сохранения."""
        hero = Hero(data["name"], data["health"], data["strength"],
                    data["agility"], data["endurance"])
        hero.stamina = data["stamina"]
        return hero


class Enemy:
    """Враг на один бой, построенный из карточки enemy_stats."""

    def __init__(self, name, stats):
        """Копирует карточку баланса в рабочие поля объекта."""
        self.name = name
        self.hp = stats["hp"]
        self.damage = stats["damage"]
        self.loot = stats["loot"]


def fight(enemy, hero, bonus=0):
    """Бой героя с врагом; возвращает (раунды, победа, добыча)."""
    rounds = []
    round_n = 0
    print(f"You descend the stairs. Out of the darkness comes {enemy.name}!")
    while enemy.hp > 0 and hero.health > 0:
        round_n += 1
        hit, crit = hero.strike(round_n)
        hit += bonus
        enemy.hp -= hit
        if crit:
            print(f"Round {round_n}: hero deals {hit:.1f} — critical! "
                  f"Enemy falls.")
            rounds.append(hit)
            break
        print(f"Round {round_n}: hero deals {hit:.1f}. "
              f"{enemy.name} health: {enemy.hp:.1f}. "
              f"{enemy.name} hits for {enemy.damage}.")
        hero.health -= enemy.damage
        rounds.append(hit)
    won = enemy.hp <= 0
    loot = enemy.loot if won else 0
    return rounds, won, loot