import random
import dungeon

# --- Блок 4: Подключение colorama с откатом ---
try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

# --- Константы ---
DUNGEON_TITLE = "DUNGEON: THE SILENT WELL"
FRAME = "==============================="

# --- Состояние игры ---
enemies = ["skeleton", "skeleton", "skeleton", "skeleton"]
log = []
gold_total = 0
ability_bonus = 0
inventory = {}

def print_leaderboard(log_data):
    if not log_data:
        print("You haven't fought yet.")
        return
    # Простой вывод последних боев
    print("Leaderboard (last hits):")
    for entry in log_data[-3:]:
        print(entry)

def safe_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter an integer.")

# --- Настройка персонажа ---
print(FRAME)
print(DUNGEON_TITLE)
print(FRAME)

hero_name = input("What is the hero's name?\n")
print(f"Welcome, {hero_name}!")
print("You enter the dungeon. Dark and damp.")

print("Hero setup.")
print("Health, strength, agility, endurance — one number per line:")
health = safe_int("")
strength = safe_int("")
agility = safe_int("")
endurance = safe_int("")

damage = strength * 2 + agility * 1.3
crit_damage = damage * 2.0
stamina = endurance * 3.5
max_health = health

print("Hero characteristics:")
print(f"Health: {health}")
print(f"Strength: {strength}")
print(f"Agility: {agility}")
print(f"Endurance: {endurance}")
print(f"Hero damage: {damage:.1f}")
print(f"Critical damage: {crit_damage:.1f}")
print(f"Stamina reserve: {int(stamina)}")

actions_count = 0
running = True

# --- Главный цикл игры ---
try:
    while running and health > 0:
        cmd = input("\nWhat do you do? (help, shop, descend, exit)\n").strip().lower()
        
        if cmd == "help":
            print("Commands: help, look, descend, shop, buy <item>, leaders, exit")
            actions_count += 1
            
        elif cmd == "look":
            print("You see stone walls and cobwebs.")
            actions_count += 1
            
        elif cmd == "descend":
            if not enemies:
                print("The dungeon is empty.")
            else:
                enemy = random.choice(enemies)
                print(f"You descend the stairs. Out of the darkness comes {enemy}!")
                
                rounds, won, health, loot = dungeon.fight(enemy, health, ability_bonus, damage, crit_damage)
                
                for r in rounds:
                    print(r)
                    log.append(r)
                    
                if won:
                    gold_total += loot
                    enemies.remove(enemy)
                    msg = f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon. Loot: {loot} gold."
                    
                    # Lib5: Красим победу в желтый
                    if COLOR:
                        print(Fore.YELLOW + msg + Style.RESET_ALL)
                    else:
                        print(msg)
                        
                    print(f"Battle: {len(rounds)} rounds.")
                else:
                    print("You have been defeated...")
            actions_count += 1
            
        elif cmd == "shop":
            print("Shop:")
            for item, price in dungeon.prices.items():
                print(f"  {item}: {price} gold")
            actions_count += 1
            
        elif cmd.startswith("buy "):
            item = cmd.split()[1]
            gold_total, ok, msg = dungeon.buy(item, gold_total, 1)
            if ok:
                inventory[item] = inventory.get(item, 0) + 1
            print(msg)
            actions_count += 1
            
        elif cmd == "leaders":
            print_leaderboard(log)
            actions_count += 1
            
        elif cmd == "exit":
            print("You climb back toward the light. The dungeon stays behind.")
            running = False
            
        else:
            print("Unknown command.")
            actions_count += 1

        # Блок 4: Зеленая строка состояния (Lib4)
        if running and health > 0:
            state = f"Health: {health} Stamina: {int(stamina)} Enemies left: {len(enemies)} Gold: {gold_total}"
            if COLOR:
                print(Fore.GREEN + state + Style.RESET_ALL)
            else:
                print(state)

except (KeyboardInterrupt, EOFError):
    print("\nInterrupted.")

# --- Финал ---
print(FRAME)
if health <= 0:
    print(f"{hero_name} has fallen in the dungeon.")
else:
    print(f"Run over, {hero_name}. Actions: {actions_count}.")
print(FRAME)