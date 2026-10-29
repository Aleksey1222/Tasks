# dungeon_game.py
# Игра: этап 10 — магазин умений
# Правило эликсира: купленное количество qty увеличивает урон на 2 * qty. 
# Bonus прибавляется к базовому урону до применения критического умножения.

import random

# --- Константы и правила игры ---
DUNGEON_TITLE = "DUNGEON: THE SILENT WELL"
FRAME = "==============================="

# Состояние и правила игры
damage = 20.5
crit_damage = 41.0
enemies = ["skeleton", "skeleton", "skeleton", "skeleton"]
log = []

# Переменные состояния забега
gold_total = 0
ability_bonus = 0


# --- Описание функций ---

def hero_hit(strike_n):
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0):
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy} emerges from the darkness!")

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        hit = hit + bonus  # Применение бонуса эликсира до/после крита зафиксировано в docstring
        enemy_hp -= hit

        line = f"Round {round_n}: hero deals {hit:.1f}."
        if crit:
            line = f"Round {round_n}: hero deals {hit:.1f} — critical!"

        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = random.randint(2, 6)
            hero_health -= blow
            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])

        print(line)

    won = enemy_hp <= 0
    loot = 10 + 5 * round_n if won else 0

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
        print("What do you do?")
        print("1 - look around\n2 - go forward\n3 - rest\n4 - listen\n5 - light a torch")
        print("6 - train\n7 - descend deeper\n8 - leaderboard\n9 - shop\n0 - exit the dungeon")

        choice = input()

        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            actions_count += 1

        match choice:
            case "1":
                print("You see stone walls and cobwebs.")
            case "2":
                print("You step forward cautiously.")
            case "3":
                print("You take a short rest.")
            case "4":
                print("You hear water dripping in the distance.")
            case "5":
                print("The torch lights up the nearby corridor.")
            case "6":
                print("How many strikes?")
                strikes = int(input())
                crit_count = 0
                total_damage = 0
                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i)
                    if crit:
                        crit_count += 1
                        print(f"Удар {i}: {hit_damage:.1f} — критический!")
                    else:
                        print(f"Удар {i}: {hit_damage:.1f}")
                    total_damage += hit_damage
            case "7":
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
            case "8":
                print_leaderboard(log)
            case "9":
                print("Shop:")
                print("1 - potion (+10 health): 10 gold")
                print("2 - torch oil (+5 stamina): 15 gold")
                print("3 - war elixir (+2 damage for the run): 40 gold")
                print("Item number (0 — not buying):")
                item = input()
                prices = (10, 15, 40)
                names = ("potion", "torch oil", "war elixir")
                
                if item in ("1", "2", "3"):
                    price = prices[int(item) - 1]
                    name = names[int(item) - 1]
                    print("Quantity (Enter for one):")
                    qty_line = input()
                    
                    if qty_line == "":
                        qty = 1
                        gold_total, ok = buy(price, gold_total)
                    else:
                        qty = int(qty_line)
                        gold_total, ok = buy(price, gold_total, quantity=qty)
                        
                    if ok:
                        if item == "1":
                            health = min(health + 10 * qty, max_health)
                        elif item == "2":
                            stamina = min(stamina + 5 * qty, max_stamina)
                        else:
                            ability_bonus += 2 * qty
                        print(f"Bought {qty} {name} for {price * qty} gold. Gold left: {gold_total}.")
                    else:
                        print(f"Not enough gold: need {price * qty}, have {gold_total}.")
                elif item != "0":
                    print("No such item in the shop.")
            case "0":
                running = False
            case _:
                print("Unknown command.")

        if health > 0 and running:
            print(f"Health: {health} Stamina: {int(stamina)} Enemies left: {len(enemies)} Gold: {gold_total}")

    if health <= 0:
        print("You fall in battle. The darkness consumes you.")
    else:
        print("You climb back toward the light. The dungeon stays behind.")

finally:
    print(FRAME)
    print(f"Run over, {hero_name}. Actions: {actions_count}.")
    print_run_summary(log)
    print(FRAME)
