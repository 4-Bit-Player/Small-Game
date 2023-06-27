import random
from decoration import colors

name = str(input("What is your name?"))

Player = {
    "name": name,
    "hp": 100,
    "hp_max": 100,
    "score": 0,
    "xp": 0,
    "lvl": 1,
    "gold": 0,
    "str": 10,
    "str_base": 10,
    "str_multi": 1,
    "def": 0,
    "def_base": 1,
    "def_multi": 1,
    "dex": 100,
    "retired": False,
    "inv": [

    ]
}

Player_default = {
    "name": name,
    "hp": 100,
    "hp_max": 100,
    "score": 0,
    "xp": 0,
    "lvl": 1,
    "gold": 0,
    "str": 10,
    "str_base": 10,
    "str_multi": 1,
    "def": 0,
    "def_base": 1,
    "def_multi": 1,
    "dex": 100,
    "retired": False,
    "inv": [

    ]
}

Equipped = {
    "Head": "",
    "Chest": "",
    "Legs": "",
    "Feet": "",
    "Sword": "",
    "Shield": "",
    "Tool": "",
}

Equipped_default = {
    "Head": "",
    "Chest": "",
    "Legs": "",
    "Feet": "",
    "Sword": "",
    "Shield": "",
    "Tool": "",
}


def restart():
    global Player
    global Player_default
    global Equipped
    global Equipped_default
    Player = Player_default
    Equipped = Equipped_default


def user_input(max_num):
    u_input = True
    u_action = input("Action:")
    full_check = range(1, max_num+1)

    while u_input:
        try:
            if 1 <= int(u_action) <= max_num:

                if int(u_action) in full_check:
                    u_input = False

                else:
                    print(f"Please select a whole number between 1 and {max_num}")
                    print("What will you do?")
                    u_action = str(input("Action:"))

            else:
                print(f"Please select a number between 1 and {max_num}")
                print("What will you do?")
                u_action = str(input("Action:"))

        except ValueError:

            print(f"Please select a number between 1 and {max_num}")
            print("What will you do?")
            u_action = str(input("Action:"))

    u_action = int(u_action) - 1
    return u_action


def show_pick_actions_dict(from_dict):
    option = 0
    for action in from_dict:
        option += 1
        print(f'{option}. {action["action_text"]}')
        try:
            price_color = colors.green if action["price"] <= Player["gold"] else colors.red
            print(f'   {colors.gold}It costs {price_color}{action["price"]} Gold{colors.reset}')
        except KeyError:
            pass


def show_pick_actions_list(from_list):
    option = 0
    for action in from_list:
        option += 1
        print(f'{option}. {action}')
    pick = int(user_input(len(from_list)))
    return pick


def random_pick_list(item_list):
    return random.randint(1, len(item_list)) - 1


def player_add_xp(xp_amount):
    global Player
    Player["xp"] += xp_amount
    lvl_up_check()


def lvl_up_check():
    global Player
    req_xp = round(90 * pow(1.1, Player["lvl"]))
    if Player["xp"] - req_xp >= 0:
        Player["xp"] -= req_xp

        lvl_up()

        print(f'You leveled up and are now {colors.turquoise}Level {Player["lvl"]}{colors.reset}!')
        lvl_up_check()


def lvl_up():
    current_missing_hp = Player["hp_max"] - Player["hp"]
    Player["hp_max"] *= 1.1
    Player["hp"] = Player["hp_max"] - current_missing_hp
    Player["str_base"] += 1
    Player["def_base"] += 1
    Player["def_multi"] += 0.1
    Player["str_multi"] += 0.1
    Player["lvl"] += 1


def player_atk():
    damage = (Player["str_base"] + equip_check("str_base")) * (Player["str_multi"] + equip_check("str_multi")) + (
        Player["str"] + equip_check("str"))
    return damage


def player_def():
    defense = (Player["def_base"] + equip_check("def_base")) * (Player["def_multi"] + equip_check("def_multi")) + (
                Player["def"] + equip_check("def"))
    return defense


def equip_check(stat):
    stat_increase = 0

    for equip in Equipped:
        if Equipped[equip] != "":
            for item_stat, amount in Equipped[equip]["player_affected_stats"].items():
                if item_stat == stat:
                    stat_increase += amount

    return stat_increase


def equip_item(item):
    global Equipped
    if Equipped[item["player_slot"]] == item:
        Equipped[item["player_slot"]] = ""
        item["equipped"] = 0

    elif Equipped[item["player_slot"]] == "":
        Equipped[item["player_slot"]] = item
        item["equipped"] = 1

    else:
        uneq_item = Equipped[item["player_slot"]]
        uneq_item["equipped"] = 0
        Equipped[item["player_slot"]] = item
        item["equipped"] = 1


def check_hp():
    if Player["hp"] >= Player["hp_max"]:
        return False
    else:
        return True


def check_hp_max():
    if Player["hp"] > Player["hp_max"]:
        Player["hp"] = Player["hp_max"]
