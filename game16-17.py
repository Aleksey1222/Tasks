"""Dungeon: The Silent Well — главный цикл игры."""

import json
import os

import dungeon

VERSION = "1.0"
SAVE_FILE = "save.json"

title = "DUNGEON: THE SILENT WELL"
frame = "=" * 31

num_to_verb = {"1": "descend", "2": "rest", "3": "potion",
               "4": "status", "5": "exit"}


def parse_command(line):
    """Возвращает пару (verb, words): глагол и слова команды."""
    cmd = line.strip().lower()
    words = cmd.split()
    if not words:
        return "", []
    verb = words[0]
    if cmd in num_to_verb:
        verb = num_to_verb[cmd]
    return verb, words


def read_int(prompt, lo, hi):
    """Читает число в диапазоне с защитой от дурака."""
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Please enter a number.")
            continue
        value = int(raw)
        if value < lo or value > hi:
            print(f"Enter a number from {lo} to {hi}.")
            continue
        return value


def write_save(hero, gold, actions, position, visited, loot):
    """Пишет состояние забега в save.json."""
    save = {"hero": hero.to_dict(), "gold": gold, "actions": actions,
            "position": position, "visited": visited, "loot": loot}
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)


def read_save():
    """Читает save.json или возвращает None, если файла нет."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, encoding="utf-8") as f:
        return json.load(f)


def main():
    """Точка входа: шапка, загрузка, настройка героя, цикл."""
    print(frame)
    print(" " + title + " ")
    print(f" v{VERSION}")
    print(frame)

    loaded = read_save()
    if loaded is not None:
        answer = input("A save was found. Continue the run? (yes/no)\n").strip().lower()
        if answer != "yes":
            loaded = None

    hero_name = input("What is the hero's name?\n").strip()
    print(f"Welcome, {hero_name}!")

    if loaded is None:
        print("You enter the dungeon. Dark and damp-smelling.")
        print("Hero setup.")
        print("Health, strength, agility, endurance — one number per line:")
        health = read_int("", 1, 999)
        strength = read_int("", 1, 99)
        agility = read_int("", 1, 99)
        endurance = read_int("", 1, 99)
        hero = dungeon.Hero(hero_name, health, strength, agility, endurance)
        gold = 0
        actions = 0
        position = 0
        visited = []
        loot = []
    else:
        hero = dungeon.Hero.from_dict(loaded["hero"])
        gold = loaded["gold"]
        actions = loaded["actions"]
        position = loaded["position"]
        visited = loaded["visited"]
        loot = loaded["loot"]

    max_health = hero.health
    enemies = list(dungeon.enemy_stats.keys())
    total_damage = 0.0
    total_rounds = 0

    print(hero)

    while True:
        print("What do you do? (number or command; help for help)")
        line = input().strip()
        verb, words = parse_command(line)
        if verb == "":
            continue
        if verb == "help":
            print("descend, rest, potion, status, exit")
        elif verb == "status":
            print(f"Health: {hero.health} Stamina: {hero.stamina} "
                  f"Enemies left: {len(enemies)} Gold: {gold}")
        elif verb == "rest":
            exhausted = hero.spend_stamina(2)
            if exhausted:
                print("You push past your limits; health pays for it.")
            hero.heal(5, max_health)
            actions += 1
        elif verb == "potion":
            hero.heal(10, max_health)
            actions += 1
        elif verb == "descend":
            if not enemies:
                print("The dungeon is empty. You won!")
                break
            enemy = enemies.pop(0)
            foe = dungeon.Enemy(enemy, dungeon.enemy_stats[enemy])
            rounds, won, gained = dungeon.fight(foe, hero, hero.agility // 2)
            actions += 1
            total_damage += sum(rounds)
            total_rounds += len(rounds)
            if won:
                gold += gained
                loot.append(f"{gained} gold")
                print(f"{enemy} defeated! {len(enemies)} enemies left "
                      f"in the dungeon. Loot: {gained} gold.")
                print(f"Battle: {len(rounds)} rounds.")
                print(f"Health: {hero.health} Stamina: {hero.stamina} "
                      f"Enemies left: {len(enemies)} Gold: {gold}")
            else:
                print("You fall. The dungeon keeps its silence.")
                break
        elif verb == "exit":
            print("You climb back toward the light. The dungeon stays behind.")
            write_save(hero, gold, actions, position, visited, loot)
            print("Progress saved.")
            if loot:
                print("Left behind in the backpack: " + ", ".join(loot) + ".")
            else:
                print("Left behind in the backpack: nothing.")
            break
        else:
            print("Unknown command.")

    print(frame)
    print(f"Run over, {hero.name}. Actions: {actions}.")
    avg = total_damage / total_rounds if total_rounds else 0.0
    print(f"Damage: {total_damage:.1f} across {total_rounds} rounds, "
          f"average {avg:.1f}.")
    print(frame)


if __name__ == "__main__":
    main()