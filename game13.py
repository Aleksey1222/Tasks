# dungeon_game.py
# Игра: этап 13 — карта подземелья
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


MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]


DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}

# Уникальный лут в комнатах
LOOT = {(1, 1): "old coin", (2, 3): "dusty potion", (3, 3): "guard's gem"}


damage = 20.5
crit_damage = 41.0
enemies = ["skeleton", "skeleton", "skeleton", "skeleton"]
log = []


gold_total = 0
ability_bonus = 0
inventory = {}

hero_r, hero_c = 4, 2
visited = {(4, 2)}
found_loot = set()

# --- Интерфейс: номера, справка, меню ---
num_to_verb = {
    "1": "look", "2": "go", "3": "rest", "4": "listen",
    "5": "torch", "6": "train", "7": "descend", "8": "leaders",
    "9": "shop", "10": "backpack", "11": "drink", 
    "12": "map", "13": "scout", "0": "exit"
}

commands = [
    "look", "go", "go <direction>", "rest", "listen", "torch", "train", "descend",
    "leaders", "shop", "backpack", "drink potion", "map", "scout",
    "buy <item> [count]", "exit"
]

MENU = [
    "What do you do? (number or command; help for help)",
    "1 - look around (look)",
    "2 - go forward (go / go <direction>)",
    "3 - rest (rest)",
    "4 - listen (listen)",
    "5 - light a torch (torch)",
    "6 - train (train)",
    "7 - descend deeper (descend)",
    "8 - leaderboard (leaders)",
    "9 - shop (shop)",
    "10 - backpack (backpack)",
    "11 - drink potion (drink)",
    "12 - show map (map)",
    "13 - scout reachable rooms (scout)",
    "0 - exit the dungeon (exit)"
]


# --- Описание функций ---

def hero_hit(strike_n, bonus=0):
    base_with_bonus = damage + bonus
    if strike_n % 3 == 0:
        return base_with_bonus * 2.0, True
    return base_with_bonus, False


def fight(enemy, hero_health, bonus=0):
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


def print_leaderboard(log_data):
    if not log_data:
        print("You haven't fought yet.")
        return

    top = sorted(log_data, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")

    worst = max(log_data, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")


def print_run_summary(log_data):
    total = sum(r[1] for r in log_data)
    rounds = len(log_data)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("Damage: 0.0 across 0 rounds, average 0.0.")


def scout(r, c, seen):
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


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

damage = strength * 2 + agility * 1.3
crit_damage = damage * 2.0
stamina = endurance * 3.5

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
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]
        else:
            verb = words[0]

        match verb:
            case "look":
                print("You see stone walls and cobwebs.")
                actions_count += 1
            case "go":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    direction_word = words[1]
                    dr, dc = DIRECTIONS[direction_word]
                    nr, nc = hero_r + dr, hero_c + dc
                    
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"You found {item}! Unique loot: {len(found_loot)}.")
                                
                        print(f"You step {direction_word}. Room ({hero_r}, {hero_c}).")
                    else:
                        print(f"Cannot go {direction_word}: wall or edge.")
                else:
                    print("You step forward cautiously.")
                actions_count += 1
            case "rest":
                print("You take a short rest.")
                actions_count += 1
            case "listen":
                print("You hear water dripping in the distance.")
                actions_count += 1
            case "torch":
                print("The torch lights up the nearby corridor.")
                actions_count += 1
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
                actions_count += 1
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
                actions_count += 1
            case "leaders":
                print_leaderboard(log)
                actions_count += 1
            case "shop":
                print("Shop:")
                for name, price in prices.items():
                    print(f"{name}: {price} gold")
                actions_count += 1
            case "backpack":
                if not inventory:
                    print("Backpack is empty.")
                else:
                    print("Backpack:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} pcs")
                actions_count += 1
            case "drink":
                print("You drink a potion.")
                actions_count += 1
            case "map":
                print("Map:")
                for i in range(len(MAP)):
                    cells = []