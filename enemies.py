import random
from player import user


def encounter(current_location):

    pick = random.randint(1, 1000)
    name = "Enemy not found"
    name = f'bugged {name}'
    enemy_lvl = 1
    enemy_hp = 1
    enemy_str = 1
    enemy_gold = 1
    enemy_def = 1
    enemy_dex = 1
    drop = {}

    try:
        for e, p in current_location["enemies"].items():

            if pick <= p:
                name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop = e()
                break
            else:
                name = f'bugged {name}'
                enemy_lvl = 1
                enemy_hp = 1
                enemy_str = 1
                enemy_gold = 1
                enemy_def = 1
                enemy_dex = 1
                drop = {}

    except TypeError:
        name = f'Type error: {current_location["enemies"]}'

    if current_location["true_weather"] == "rainy":
        enemy_lvl *= 1.2
        enemy_hp *= 1.2
        enemy_str *= 1.2
        enemy_gold *= 1.2
        enemy_def *= 1.2
        enemy_dex *= 1.2
        enemy_xp = (enemy_hp / 10 + enemy_str / 2 + enemy_dex / 10 + 5) * 1.2

    else:
        enemy_xp = enemy_hp / 10 + enemy_str / 2 + enemy_dex / 10 + 5

    enemy = {
        "name": name,
        "hp": enemy_hp,
        "str": round(enemy_str, 1),
        "xp": round(enemy_xp),
        "gold": round(enemy_gold, 1),
        "lvl": round(enemy_lvl),
        "def": round(enemy_def, 1),
        "dex": enemy_dex,
        "drop": drop
        }
    print(enemy)
    return enemy


def wild_boar():
    name = "Wild Boar"
    enemy_lvl = max(1, round(random.uniform(0.3 * user.Player["lvl"], 1.5 * user.Player["lvl"])))
    enemy_hp = random.uniform(50 + (2 * enemy_lvl), 80 + (enemy_lvl * 3)) * (1 + user.Player["score"] / 700)
    enemy_str = random.uniform(6, 10) * (1 + user.Player["score"] / 500) * (1 + enemy_lvl * .2)
    enemy_gold = random.uniform(10, 15) * (1 + enemy_lvl * 0.3)
    enemy_def = random.randint(1, 3 * enemy_lvl)
    enemy_dex = random.uniform(int(50 * (1 + enemy_lvl / 80)), int(80 * (1 + enemy_lvl / 40)))
    drop = {
        "Boar Hide": {3: 100, 2: 300, 1: 500},
        "Boar Tusk": {2: 100, 1: 200},
    }
    return name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop


def big_wild_boar():
    name = "Big Wild Boar"
    enemy_lvl = max(1, round(random.uniform(user.Player["lvl"], 2 * (1 + user.Player["lvl"]))))
    enemy_hp = random.uniform(60 + (2 * enemy_lvl), 85 + (enemy_lvl * 3)) * (1 + user.Player["score"] / 700)
    enemy_str = random.uniform(6, 10) * (1 + user.Player["score"] / 500) * (1 + enemy_lvl * .2)
    enemy_gold = random.uniform(10, 15) * (1 + enemy_lvl * 0.5)
    enemy_def = random.uniform(1, 3 * enemy_lvl)
    enemy_dex = random.uniform(int(50 * (1 + enemy_lvl / 80)), int(80 * (1 + enemy_lvl / 40)))
    drop = {
        "Tough Boar Hide": {3: 100, 2: 300, 1: 700},
        "Large Boar Tusk": {2: 100, 1: 300},
    }
    return name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop
