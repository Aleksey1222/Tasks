import random
import json
import os

# ============================================================
# КОНСТАНТЫ
# ============================================================
MAP_W, MAP_H = 5, 5
WALL, FLOOR, STAIRS, HERO, ENEMY = "#", ".", "S", "@", "E"

MENU = """
What do you do? (number or command; help for help)
  1 - move up
  2 - move down
  3 - move left
  4 - move right
  5 - attack
  6 - rest
  7 - search
Commands: help, map, status, inventory, exit, newgame
"""

commands = ["help", "map", "status", "inventory", "exit", "newgame"]


# ============================================================
# ЭТАП 15: СОХРАНЕНИЕ
# ============================================================
def write_save():
    """Собирает состояние забега и пишет его в save.json.
    Кортежи и множества превращает в списки: JSON их не знает.
    Возвращает None.
    """
    save = {}
    save["hero"] = hero_name
    save["health"] = health
    save["stamina"] = stamina
    save["gold"] = gold_total
    save["actions"] = actions
    save["enemies"] = enemies
    save["position"] = [hero_r, hero_c]
    save["visited"] = [list(p) for p in visited]
    save["loot"] = sorted(found_loot)

    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================
def make_dungeon():
    """Генерирует карту: рамка из стен, внутри пол, лестница."""
    grid = [[WALL] * MAP_W for _ in range(MAP_H)]
    for r in range(1, MAP_H - 1):
        for c in range(1, MAP_W - 1):
            grid[r][c] = FLOOR
    grid[MAP_H - 2][MAP_W - 2] = STAIRS
    return grid


def make_enemies(count):
    """Список врагов: [name, health, damage]."""
    names = ["Goblin", "Skeleton", "Slime", "Bat", "Rat"]
    result = []
    for i in range(count):
        name = random.choice(names) + f" #{i + 1}"
        result.append([name, random.randint(10, 25), random.randint(2, 6)])
    return result


def render_map(grid, hero_r, hero_c):
    """Печатает карту с героем и лестницей."""
    lines = []
    for r in range(MAP_H):
        row = []
        for c in range(MAP_W):
            if r == hero_r and c == hero_c:
                row.append(HERO)
            else:
                row.append(grid[r][c])
        lines.append(" ".join(row))
    return "\n".join(lines)


def hero_hit(damage):
    """Наносит урон герою. Возвращает новый health."""
    global health
    health -= damage
    return health


# ============================================================
# ЗАГОЛОВОК
# ============================================================
print("===============================")
print("DUNGEON: THE SILENT WELL")
print("===============================")

# ============================================================
# ЭТАП 15: ЗАГРУЗКА (до вопроса об имени!)
# ============================================================
loaded = None
if os.path.exists("save.json"):
    print("A save was found. Continue the run? (yes/no)")
    answer = input().strip().lower()
    if answer == "yes":
        try:
            with open("save.json", encoding="utf-8") as f:
                loaded = json.load(f)
        except json.JSONDecodeError:
            print("The save is corrupted. Starting a new run.")
            loaded = None


# ============================================================
# НАСТРОЙКА ИЛИ ВОССТАНОВЛЕНИЕ
# ============================================================
if loaded is None:
    # --- Новый забег: знакомство, настройка, формуляр ---
    print("What is the hero's name?")
    hero_name = input().strip()
    if hero_name == "":
        hero_name = "Anya"

    health = 100
    stamina = 50
    gold_total = 0
    actions = 0
    enemies = make_enemies(3)
    grid = make_dungeon()
    hero_r, hero_c = 1, 1
    visited = {(hero_r, hero_c)}
    found_loot = set()
    outcome = None

    print(f"Welcome, {hero_name}.")
    print(f"Health: {health}, stamina: {stamina}, gold: {gold_total}.")
    print(f"Enemies in the dungeon: {len(enemies)}.")
else:
    # --- Продолжение: восстановление из save.json ---
    hero_name = loaded["hero"]
    health = loaded["health"]
    stamina = loaded["stamina"]
    gold_total = loaded["gold"]
    actions = loaded["actions"]
    enemies = loaded["enemies"]
    hero_r, hero_c = loaded["position"]
    visited = {tuple(p) for p in loaded["visited"]}
    found_loot = set(loaded["loot"])
    grid = make_dungeon()
    outcome = None
    print(f"Run continued: health {health}, gold {gold_total}, enemies left {len(enemies)}.")


# ============================================================
# ГЛАВНЫЙ ЦИКЛ
# ============================================================
running = True
try:
    while running:
        print(MENU)
        raw = input().strip()

        # --- команды ---
        if raw in commands:
            match raw:
                case "help":
                    print("Move with 1-4, attack with 5, rest with 6, search with 7.")
                    print("Commands: help, map, status, inventory, exit, newgame.")
                case "map":
                    print("Map:")
                    print(render_map(grid, hero_r, hero_c))
                case "status":
                    print(f"{hero_name}: health {health}, stamina {stamina}, gold {gold_total}, actions {actions}.")
                case "inventory":
                    if found_loot:
                        print("Loot: " + ", ".join(sorted(found_loot)) + ".")
                    else:
                        print("Left behind in the backpack: nothing.")
                case "exit":
                    print("You climb back toward the light. The dungeon stays behind.")
                    write_save()
                    print("Progress saved.")
                    outcome = "exit"
                    running = False
                case "newgame":
                    if os.path.exists("save.json"):
                        os.remove("save.json")
                        print("Save destroyed. The next run starts fresh.")
                    else:
                        print("No save to destroy.")
                    continue
            continue

        # --- числовые действия ---
        if not raw.isdigit():
            print("Unknown command. Type help.")
            continue

        action = int(raw)
        actions += 1
        moved = False
        nr, nc = hero_r, hero_c

        match action:
            case 1:
                nr -= 1
            case 2:
                nr += 1
            case 3:
                nc -= 1
            case 4:
                nc += 1
            case 5:
                # атака
                if enemies:
                    target = enemies[0]
                    dmg = random.randint(8, 18)
                    target[1] -= dmg
                    print(f"You hit {target[0]} for {dmg}. Its health: {max(0, target[1])}.")
                    if target[1] <= 0:
                        print(f"{target[0]} falls.")
                        enemies.pop(0)
                        gold_total += random.randint(5, 15)
                else:
                    print("No enemies left here.")
            case 6:
                # отдых
                stamina = min(50, stamina + 10)
                print(f"You rest. Stamina: {stamina}.")
            case 7:
                # поиск
                if random.random() < 0.5:
                    item = random.choice(["torch", "rope", "coin", "herb"])
                    found_loot.add(item)
                    print(f"You found: {item}.")
                else:
                    print("You search but find nothing.")
            case _:
                print("Unknown action.")
                actions -= 1
                continue

        # --- движение ---
        if action in (1, 2, 3, 4):
            if 0 <= nr < MAP_H and 0 <= nc < MAP_W and grid[nr][nc] != WALL:
                hero_r, hero_c = nr, nc
                visited.add((hero_r, hero_c))
                moved = True
                print(f"You move to ({hero_r}, {hero_c}).")
            else:
                print("A wall blocks the way.")

        # --- враг отвечает, если живой и герой рядом ---
        if enemies and moved and random.random() < 0.4:
            enemy = enemies[0]
            dmg = random.randint(enemy[2] // 2, enemy[2])
            hero_hit(dmg)
            print(f"{enemy[0]} hits you for {dmg}. Health: {health}.")

        # --- проверка гибели ---
        if health <= 0:
            print(f"{hero_name} falls. The dungeon claims another seeker.")
            if os.path.exists("save.json"):
                os.remove("save.json")
            outcome = "death"
            running = False

        # --- проверка лестницы ---
        if (hero_r, hero_c) == (MAP_H - 2, MAP_W - 2) and not enemies:
            print("You reach the stairs and escape the dungeon!")
            outcome = "win"
            if os.path.exists("save.json"):
                os.remove("save.json")
            running = False

except KeyboardInterrupt:
    print()
    print("The player ended the session.")
    write_save()
    outcome = "interrupt"

finally:
    print("===============================")
    if outcome == "death":
        print(f"Run over, {hero_name}. Actions: {actions}.")
        print("The dungeon keeps its dead.")
    elif outcome == "win":
        print(f"Run over, {hero_name}. Actions: {actions}.")
        print(f"You escaped with {gold_total} gold!")
    elif outcome == "exit":
        print(f"Run over, {hero_name}. Actions: {actions}.")
    else:
        print(f"Run over, {hero_name}. Actions: {actions}.")
    if found_loot:
        print("Loot: " + ", ".join(sorted(found_loot)) + ".")
    else:
        print("Left behind in the backpack: nothing.")
    print("===============================")