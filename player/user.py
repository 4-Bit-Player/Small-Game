import random
from decoration import deco, colors

Player = {
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


def restart():
    global Player
    global Player_default
    Player = Player_default


def check_player_stats():
    deco.clear_l(1)
    print(f'You are {colors.turquoise}Level {Player["lvl"]}{colors.reset}.')
    print(f'You have {colors.pink}{Player["xp"]} / {round(90 * pow(1.1, Player["lvl"]))} XP{colors.reset}.')
    print(f'Your total strength is {colors.red}{round(player_atk(), 1)} atk{colors.reset}.')
    print(f'You have {colors.green}{round(Player["hp"], 1)} / {round(Player["hp_max"], 1)}{colors.reset} HP.')
    print(f'You have {colors.gray}{round(Player["def"], 1)} Defense{colors.reset}.')
    print(f'You have {colors.gold}{round(Player["gold"], 1)} Gold{colors.reset}.')
    print(f'You have {colors.light_blue}{round(Player["score"], 1)} Points{colors.reset}.')


def user_input(max_num):
    u_input = True
    u_action = str(input("Action:"))
    full_check = range(1, max_num+1)

    while u_input:
        try:
            if "1" <= u_action <= str(max_num):

                if float(u_action) in full_check:
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
    pick = int(user_input(len(from_dict)))
    return pick


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
    damage = Player["str_base"] * Player["str_multi"] + Player["str"]
    return damage


def player_def():
    defense = Player["def_base"] * Player["def_multi"] + Player["def"]
    return defense


def check_hp():
    if Player["hp"] >= Player["hp_max"]:
        return False
    else:
        return True


def check_hp_max():
    if Player["hp"] > Player["hp_max"]:
        Player["hp"] = Player["hp_max"]
