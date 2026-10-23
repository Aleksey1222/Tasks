# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ»
# Автор: Алексей Семерич
# Дата: 21.09.2026
#
# Пункт 4 — «прислушаться»: герой замирает
# и слушает, что происходит в темноте. Пока
# пункт только выводится в меню — обрабатывать
# его будем на третьем занятии.
# ================================================


import random

print("========================")
print(" ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ")
print("========================")

name = input("What is the hero's name? ")

health = 100
stamina = 20
enemies = ["skeleton", "goblin", "orc", "troll"]
log = []

print(f"Welcome, {name}. Health: {health} Stamina: {stamina}")

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
        break
    elif choice == "1":
        print("You look around. The walls are silent.")
    elif choice == "2":
        print("You go forward carefully.")
    elif choice == "3":
        stamina = min(stamina + 5, 20)
        print(f"You rest. Stamina: {stamina}")
    elif choice == "4":
        print("You listen. Something moves in the dark.")
    elif choice == "5":
        if stamina >= 5:
            stamina -= 5
            print(f"You light a torch. Stamina: {stamina}")
        else:
            print("Not enough stamina to light a torch.")
    elif choice == "6":
        print("You train. Your muscles remember the weight of the sword.")
    elif choice == "7":
        if not enemies:
            print("You descend the stairs. But the dungeon is empty.")
        else:
            enemy = random.choice(enemies)
            enemy_hp = random.uniform(20.0, 40.0)
            round_n = 0
            rounds = []
            while health > 0 and enemy_hp > 0:
                round_n += 1
                hit = random.uniform(10.0, 25.0)
                enemy_hp -= hit
                line = f"Round {round_n}: hero deals {hit:.1f}. Enemy health: {max(enemy_hp, 0):.1f}."
                rounds.append(line)
                if enemy_hp <= 0:
                    break
                dmg = random.randint(3, 7)
                health -= dmg
                line = f"Round {round_n}: {enemy.capitalize()} hits for {dmg}."
                rounds.append(line)
            for r in rounds:
                log.append(r)
                print(r)
            if enemy_hp <= 0:
                enemies.remove(enemy)
                print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left.")
            else:
                print("You fall. The dungeon stays behind.")
                break
    elif choice == "8":
        print("Leaderboard:")
        print("1 - Anya ....... 3 enemies")
        print("2 - Boris ...... 2 enemies")
        print("3 - Vera ....... 1 enemy")
    else:
        print("Unknown command.")

    print(f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)}")

print(f"You climb back toward the light. The dungeon stays behind.")