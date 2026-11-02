# dungeon_game.py
# Игра: этап 12 — меню понимает команды
# Правило эликсира: купленное количество qty увеличивает урон на 2 * qty.
# Bonus прибавляется к базовому урону до применения критического умножения.

import random

# --- Константы и правила игры ---
DUNGEON_TITLE = "DUNGEON: THE SILENT WELL"
FRAME = "==============================="

prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "ghoul": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}

# Состояние и правила игры
damage = 20.5
crit_damage = 41.0
enemies = ["skeleton", "skeleton", "skeleton", "skeleton"]
log = []

# Переменные состояния забега
gold_total = 0
ability_bonus = 0
inventory = {}

# --- Интерфейс: номера, справка, меню ---
num_to_verb = {"1": "look", "2": "go", "3": "rest", "4": "listen",
               "5": "torch", "6": "train", "7": "descend", "8": "leaders",
               "9": "shop", "10": "backpack", "11": "drink", "0": "exit"}

commands = ["look", "go", "rest", "listen", "torch", "train", "descend",
            "leaders", "shop", "backpack", "drink potion",
            "buy <item> [count]", "exit"]

MENU = ["What do you do? (number or command; help for help)",
        "1 - look around (look)",
        "2 - go forward (go)",
        "3 - rest (rest)",
        "4 - listen (listen)",
        "5 - light a torch (torch)",
        "6 - train (train)",
        "7 - descend deeper (descend)",
        "8 - leaderboard (leaders)",
        "9 - shop (shop)",
        "10 - backpack (backpack)",
        "11 - drink potion (drink)",
        "0 - exit the dungeon (exit)"]


# --- Описание функций ---

def hero_hit(strike_n, bonus=0):
    base_with_bonus = damage + bonus
    if strike_n % 3 == 0:
        return base_with_bonus * 2.0, True
    return base_with_bonus, False


def fight(enemy, hero_health, bonus=0):
    """Бой с enemy до гибели одного из двоих.
    Карточка врага берётся из enemy_stats по имени: нужны ключи
    hp, damage, loot. Печатает строки раундов.
    Возвращает (rounds, won, hero_health, loot).
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy} emerges from the darkness!")

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n, bonus=bonus)
        enemy_hp -= hit

        line = f"Round {round_n}: hero deals {hit:.1f}."
        if crit:
            line = f"Round {round_n}: hero deals {hit:.1f} — critical!"

        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = stats["damage"]
            hero_health -= blow
            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])

        print(line)

    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0

    return rounds, won, hero_health, loot


def buy(price, gold, quantity=1):
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


def print_leaderboard(log):
    if not log:
        print("You haven't fought yet.")
        return

    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")

    worst = max(log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")


def print_run_summary(log):
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")


# --- Настройка персонажа ---

print(FRAME)
print(DUNGEON_TITLE)
print(FRAME)

hero_name = input("What is the hero's name?\n")
print(f"Welcome, {hero_name}!")
print("You enter the dungeon. Dark and damp.")

print("Hero setup.")
print("Health, strength, agility, endurance — one number per line:")
health = int(input())
strength = int(input())
agility = int(input())
endurance = int(input())

# Первичный расчет характеристик
damage = strength * 2 + agility * 1.3
crit_damage = damage * 2.0
stamina = endurance * 3.5

# Фиксация потолков характеристик для магазина
max_health = health
max_stamina = stamina

print("Hero characteristics:")
print("Health:")
print(health)
print("Strength:")
print(strength)
print("Agility:")
print(agility)
print("Endurance:")
print(endurance)

print(f"Hero damage: {damage:.1f}")
print(f"Critical damage: {crit_damage:.1f}")
print(f"Stamina reserve: {int(stamina)}")

actions_count = 0
running = True

# --- Главный цикл игры ---

try:
    while running and health > 0:
        print("\n".join(MENU))
        print()

        line = input()
        cmd = line.strip().lower()
        while cmd == "":
            print("Empty command. Type a command or number.")
            line = input()
            cmd = line.strip().lower()

        words = cmd.split()
        verb = words[0]
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]

        match verb:
            case "look":
                print("You see stone walls and cobwebs.")
            case "go":
                print("You step forward cautiously.")
            case "rest":
                print("You take a short rest.")
            case "listen":
                print("You hear water dripping in the distance.")
            case "torch":
                print("The torch lights up the nearby corridor.")
            case "train":
                print("How many strikes?")
                strikes = int(input())
                total_damage = 0
                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i, bonus=ability_bonus)
                    if crit:
                        print(f"Удар {i}: {hit_damage:.1f} — критический!")
                    else:
                        print(f"Удар {i}: {hit_damage:.1f}")
                    total_damage += hit_damage
            case "descend":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health, loot = fight(enemy, health, bonus=ability_bonus)
                    for r in rounds:
                        log.append(r)
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon. Loot: {loot} gold.")
                        print(f"Battle: {len(rounds)} rounds.")
            case "leaders":
                print_leaderboard(log)
            case "shop":
                print("Shop:")
                for name, price in prices.items():
                    print(f"{name}: {price} gold")
            case "backpack":
                if not inventory:
                    print("Backpack is empty.")
                else:
                    print("Backpack:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} pcs")
            case "help":
                print("Commands: " + ", ".join(commands) + ".")
                print("Numbers 0-11 work as before.")
            case "buy":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])
                if item == "":
                    print("Buy what? Type: buy <item>.")
                    continue
                if item not in prices:
                    print("No such item in the shop.")
                    continue
                gold_total, ok = buy(prices[item], gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    if item == "war_elixir":
                        ability_bonus += 2 * qty
                    print(f"Bought {qty} {item} for {prices[item] * qty} gold. Gold left: {gold_total}.")
                else:
                    print(f"Not enough gold: need {prices[item] * qty}, have {gold_total}.")
            case "drink":
                item = " ".join(words[1:]) or "potion"
                if inventory.get(item, 0) == 0:
                    print(f"No {item} in the backpack.")
                else:
                    health = min(health + 10, max_health)
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    print(f"You drink a {item}. Health: {health}. Potions left: {inventory.get(item, 0)}.")
            case "exit":
                print("You climb back toward the light. The dungeon stays behind.")
                running = False
            case _:
                print(f"Don't understand command: '{line.strip()}'. Type 'help'.")
                continue

        actions_count += 1
        if health > 0 and running:
            print(f"Health: {health} Stamina: {int(stamina)} Enemies left: {len(enemies)} Gold: {gold_total}")

    if health <= 0:
        print("You fall in battle. The darkness consumes you.")
    else:
        print("You climb back toward the light. The dungeon stays behind.")

finally:
    if inventory:
        print("Left behind in the backpack:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} pcs")
    else:
        print("Left behind in the backpack: nothing.")

    print(FRAME)
    print(f"Run over, {hero_name}. Actions: {actions_count}.")
    print_run_summary(log)
    print(FRAME)