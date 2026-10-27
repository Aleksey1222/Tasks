
# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ»
# Автор: Алексей Семерич
# Дата: 21.09.2026
#
# Этап 9 — разбор боя на функции
# ================================================

import random

# --- Константы и настройки игры ---
TITLE = "DUNGEON: THE SILENT WELL"
FRAME = "==============================="

# Глобальные правила игры (базовые характеристики)
damage = 20.5
crit_damage = 41.0
stamina_max = 14

# --- Инициализация состояния игры ---
print("========================")
print(" ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ")
print("========================")

name = input("What is the hero's name?\n")
print(f"Welcome, {name}!")
print("You enter the dungeon. Dark.")

# Первоначальная настройка характеристик
health = 100
stamina = stamina_max
enemies = ["skeleton", "goblin", "orc", "troll"]
log = [] 
actions_count = 0


# --- Определение функций (Блоки 1-4) ---

def hero_hit(strike_n):
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health):
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy} emerges from the darkness!")

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        enemy_hp -= hit

        line = f"Round {round_n}: hero deals {hit:.1f}"
        if crit:
            line += " — critical!"

        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = random.randint(2, 6)
            hero_health -= blow
            line += f" {enemy.capitalize()} health: {max(enemy_hp, 0):.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])

        print(line)

    return rounds, enemy_hp <= 0, hero_health


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


# --- Главный цикл игры ---
try:
    while True:
        print("What do you do?")
        print("1 - look around")
        print("2 - go forward")
        print("3 - rest")
        print("4 - listen")
        print("5 - light a torch")
        print("6 - train")
        print("7 - descend deeper")
        print("8 - leaderboard")
        print("0 - exit the dungeon")
        
        choice = input()

        if choice == "0":
            print("You climb back toward the light. The dungeon stays behind.")
            break
            
        elif choice == "1":
            actions_count += 1
            print("You look around. The walls are silent.")
            
        elif choice == "2":
            actions_count += 1
            print("You go forward carefully.")
            
        elif choice == "3":
            actions_count += 1
            stamina = min(stamina + 5, stamina_max)
            print(f"You rest. Stamina: {stamina}")
            
        elif choice == "4":
            actions_count += 1
            print("You listen. Something moves in the dark.")
            
        elif choice == "5":
            actions_count += 1
            if stamina >= 5:
                stamina -= 5
                print(f"You light a torch. Stamina: {stamina}")
            else:
                print("Not enough stamina to light a torch.")
                
        elif choice == "6":
            actions_count += 1
            strikes = 5
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
                
        elif choice == "7":
            actions_count += 1
            if not enemies:
                print("You descend the stairs. But the dungeon is empty.")
            else:
                enemy = random.choice(enemies)
                rounds, won, health = fight(enemy, health)
                
                for r in rounds:
                    log.append(r)
                    
                if won:
                    enemies.remove(enemy)
                    print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                    
                print(f"Battle: {len(rounds)} rounds.")
                
                if health <= 0:
                    print("You fall. The dungeon stays behind.")
                    break

        elif choice == "8":
            print_leaderboard(log)
            
        else:
            print("Unknown command.")

        print(f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)}")

finally:
    # Гарантированный вывод финального блока (при выходе, смерти или Ctrl+C)
    print(FRAME)
    print(f"Run over, {name}. Actions: {actions_count}.")
    print_run_summary(log)
    print(FRAME)

