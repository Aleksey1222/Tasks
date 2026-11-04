"""
Правила игры: бой, магазин, карточки врагов.
Модуль содержит боевые функции (hero_hit, fight), экономику (buy, prices)
и данные врагов (enemy_stats).
Выбор случайного врага оставлен в game.py.
"""
import random

# Данные правил
prices = {
    "potion": 15,
    "war_elixir": 30
}

enemy_stats = {
    "skeleton": {"health": 45, "damage": 6, "loot": 25},
    "goblin":   {"health": 35, "damage": 5, "loot": 15},
    "orc":      {"health": 60, "damage": 10, "loot": 40}
}

def hero_hit(strike_n, damage, crit_damage):
    """Урон героя в удар strike_n; возвращает пару (hit, crit)."""
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False

def fight(enemy, hero_health, bonus, damage, crit_damage):
    """Симуляция боя с врагом. Возвращает (rounds, won, health, loot)."""
    stats = enemy_stats[enemy]
    enemy_health = stats["health"]
    enemy_damage = stats["damage"]
    loot = stats["loot"]
    
    rounds = []
    health = hero_health
    round_num = 1
    
    while health > 0 and enemy_health > 0:
        # Удар героя
        hit, crit = hero_hit(round_num, damage + bonus, crit_damage + bonus)
        enemy_health -= hit
        crit_text = " — critical!" if crit else "."
        
        if enemy_health <= 0:
            rounds.append(f"Round {round_num}: hero deals {hit:.1f}{crit_text} Enemy falls.")
            break
            
        # Ответный удар врага
        health -= enemy_damage
        rounds.append(f"Round {round_num}: hero deals {hit:.1f}{crit_text} {enemy} health: {max(0, enemy_health):.1f}. {enemy} hits for {enemy_damage}.")
        round_num += 1

    won = enemy_health <= 0 and health > 0
    if not won:
        loot = 0
        health = 0
        
    return rounds, won, health, loot

def buy(item, gold, qty=1):
    """Покупка предмета. Возвращает (new_gold, ok, message)."""
    if item not in prices:
        return gold, False, "Unknown item."
    total_cost = prices[item] * qty
    if gold < total_cost:
        return gold, False, "Not enough gold."
    return gold - total_cost, True, f"Bought {item} x{qty} for {total_cost} gold."

# Самотест модуля (Lib2)
if __name__ == "__main__":
    rounds, won, hp, loot = fight("skeleton", 100, 0, 20.5, 41.0)
    print(f"self-test: {len(rounds)} rounds, won={won}, loot={loot}")