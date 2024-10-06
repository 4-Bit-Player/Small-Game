import random
from copy import deepcopy
import items.armor
from decoration import colors


test = False
Version = "0.6.8"
Compatible_versions = ["0.6.8"]
Player_default = {
    "name": "",
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
    "deaths": 0,
    "inv": [

    ]
}

Player = deepcopy(Player_default)
character_loaded = False
deaths = 0
highscore = 0

settings = {
    "delete_save_on_death": 0,
    "centered_screen": False,
}

Equipped_default:dict = {
    "Head": "",
    "Chest": "",
    "Legs": "",
    "Feet": "",
    "Sword": "",
    "Shield": "",
    "Tool": "",
}

Equipped = deepcopy(Equipped_default)


def restart():
    global Player
    global Equipped
    global character_loaded
    global deaths
    if test:
        Player = deepcopy(Test_Player)
    else:
        Player = deepcopy(Player_default)
    Equipped = deepcopy(Equipped_default)
    character_loaded = False
    deaths = 0


def combining_words(actions, iteration):
    checking = True
    while checking:
        if actions[iteration] in ["the", "at", "to", "for", "in"]:
            iteration += 1
        else:
            return iteration


def user_input_new(options):
    print(options)
    u_input = True
    while u_input:
        iteration = 0
        u_action = str(input("Action:")).lower()
        actions = u_action.split()
        if actions[iteration] in ["go", "walk", "run", "jog"]:
            print("Yay!")

        if actions[iteration] in ["check", "look", "inspect"]:
            iteration += 1
            iteration = combining_words(actions, iteration)
            if actions[iteration] in ["around", "surrounding", "area"]:
                for option in options["list_of_actions"]:
                    if option["action_text"] == "Look around.":
                        print("nice! :)")


def user_input(max_num):
    u_input = True
    u_action = input("Action:")
    actual_action = 0
    while u_input:
        try:
            actual_action = int(u_action)
            if 1 <= actual_action <= max_num:
                u_input = False

            else:
                print(f"Please select a number between 1 and {max_num}")
                print("What will you do?")
                u_action = str(input("Action:"))

        except ValueError:
            print(f"Please select a number between 1 and {max_num}")
            print("What will you do?")
            u_action = str(input("Action:"))

    return actual_action - 1


def return_pick_actions_dict(from_dict):
    option = 0
    out = []
    for action in from_dict:
        option += 1
        out.append(f'{action["action_text"]}')
        if "price" in action:
            price_color = colors.green if action["price"] <= Player["gold"] else colors.red
            out.append([f'   {colors.gold}It costs {price_color}{action["price"]} Gold{colors.reset}'])
    return out


def player_add_xp(xp_amount):
    global Player
    Player["xp"] += xp_amount
    return lvl_up_check()


def lvl_up_check(overfow=""):
    global Player
    req_xp = round(90 * pow(1.1, Player["lvl"]))
    if Player["xp"] - req_xp >= 0:
        Player["xp"] -= req_xp

        lvl_up()

        overfow += f'You leveled up and are now {colors.turquoise}Level {Player["lvl"]}{colors.reset}!\n'
        return lvl_up_check(overfow)
    return overfow


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
    damage = (Player["str_base"] + equip_check("str_base")) * (Player["str_multi"] + equip_check("str_multi")/100) + (
        Player["str"] + equip_check("str"))
    return damage


def player_def():
    defense = (Player["def_base"] + equip_check("def_base")) * (Player["def_multi"] + equip_check("def_multi")/100) + (
                Player["def"] + equip_check("def"))
    return defense


def player_dex():
    return Player["dex"] + equip_check("dex")


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


if test:
    # noinspection PyRedeclaration
    Player = {
        "name": "",
        "hp": 1000,
        "hp_max": 1000,
        "score": 0,
        "xp": 0,
        "lvl": 1,
        "gold": 1000,
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
