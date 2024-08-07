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
                if e in all_enemies:
                    name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop = all_enemies[e]()
                else:
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
        "lvl": round(enemy_lvl),
        "hp": round(enemy_hp, 1),
        "max_hp": round(enemy_hp, 1),
        "str": round(enemy_str, 1),
        "def": round(enemy_def, 1),
        "xp": round(enemy_xp),
        "gold": round(enemy_gold, 1),
        "dex": round(enemy_dex, 1),
        "drop": drop
        }
    return enemy


def wild_boar():
    name = "Wild Boar"
    enemy_lvl = max(1, round(random.uniform(0.3 * user.Player["lvl"], 1.5 * user.Player["lvl"])))
    enemy_hp = random.uniform(50 + (2 * enemy_lvl), 80 + (enemy_lvl * 3)) * (1 + user.Player["lvl"] / 10)
    enemy_str = random.uniform(6, 10) * (1 + user.Player["lvl"] / 8) * (1 + enemy_lvl * .2)
    enemy_gold = random.uniform(10, 15) * (1 + enemy_lvl * 0.1)
    enemy_def = random.randint(1, 3 * enemy_lvl)
    enemy_dex = random.uniform(int(50 * (1 + enemy_lvl / 80)), int(80 * (1 + enemy_lvl / 40)))
    drop = {
        "Boar Hide": {3: 100, 2: 300, 1: 500},
        "Boar Tusk": {2: 100, 1: 200},
    }
    return name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop


def big_wild_boar():
    name = "Big Wild Boar"
    enemy_lvl = max(4, round(0.8 * random.uniform(user.Player["lvl"], 1.5 * (1 + user.Player["lvl"]))))
    enemy_hp = random.uniform(60 + (2 * enemy_lvl), 85 + (enemy_lvl * 3)) * (1 + user.Player["lvl"] / 9)
    enemy_str = random.uniform(6, 10) * (1 + user.Player["lvl"] / 6) * (1 + enemy_lvl * .2)
    enemy_gold = random.uniform(10, 15) * (1 + enemy_lvl * 0.1)
    enemy_def = random.uniform(1 * enemy_lvl, 3 * enemy_lvl)
    enemy_dex = random.uniform(int(50 * (1 + enemy_lvl / 80)), int(80 * (1 + enemy_lvl / 40)))
    drop = {
        "Tough Boar Hide": {3: 100, 2: 300, 1: 700},
        "Large Boar Tusk": {2: 100, 1: 300},
    }
    return name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop


def skeleton():
    name = "Skeleton"
    enemy_lvl = max(7, round(random.uniform(0.7 * user.Player["lvl"], 1.3 * (1 + user.Player["lvl"]))))
    enemy_hp = random.uniform(50 + (2 * enemy_lvl), 70 + (enemy_lvl * 3)) * (1 + user.Player["lvl"] / 9)
    enemy_str = random.uniform(6, 10) * (1 + user.Player["lvl"] / 5) * (1 + enemy_lvl * .2)
    enemy_gold = random.uniform(10, 15) * (1 + enemy_lvl * 0.1)
    enemy_def = random.uniform(20*(1+enemy_lvl/10), 30 * (1+enemy_lvl/10))
    enemy_dex = random.uniform(int(50 * (1 + enemy_lvl / 60)), int(80 * (1 + enemy_lvl / 40)))
    drop = {
        "Bone": {3: 100, 2: 200, 1: 600},
        "Rusty Sword": {1: 20},
        "Rusty Shield": {1: 20},
    }
    return name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop


def ogre():
    name = "Ogre"
    enemy_lvl = max(20, round(random.uniform(0.7 * user.Player["lvl"], 1.5 * (1 + user.Player["lvl"]))))
    enemy_hp = random.uniform(80 + (2 * enemy_lvl), 110 + (enemy_lvl * 3)) * (1 + user.Player["lvl"] / 9)
    enemy_str = random.uniform(10, 15) * (1 + user.Player["lvl"] / 5) * (1 + enemy_lvl * .2)
    enemy_gold = random.uniform(10, 15) * (1 + enemy_lvl * 0.1)
    enemy_def = random.uniform(20, 3 * enemy_lvl)
    enemy_dex = random.uniform(int(50 * (1 + enemy_lvl / 90)), int(60 * (1 + enemy_lvl / 60)))
    drop = {
        "Giant Club": {1: 700},
        "Shiny Crystal": {1: 700}
    }
    return name, enemy_lvl, enemy_hp, enemy_str, enemy_gold, enemy_def, enemy_dex, drop



all_enemies = {
    "wild_boar": wild_boar,
    "big_wild_boar": big_wild_boar,
    "skeleton": skeleton,
    "ogre": ogre,

}
