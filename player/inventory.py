from player import user
import copy
from decoration import deco, colors


def open_inventory():
    inv_open = True
    deco.clear_l(s="", clear_all=1)
    deco.player_hud()

    while inv_open:

        deco.print_header("Inventory")

        if len(user.Player["inv"]) <= 0:
            deco.clear_l()
            print("Your inventory is currently empty.")
            print("1. Close inventory")
            deco.clear_l()

        else:
            print("1. Close inventory")
            print("2. Inspect item")
            for i, item in enumerate(user.Player["inv"]):

                print(f'{i+3}. {item["item_name"]}{(" x "+str(item["item_amount"])) if item["item_amount"]>1 else ""}')

        pick = user.user_input(len(user.Player["inv"]) + 2)

        if not pick:
            inv_open = False

        elif pick == 1:
            inv_inspect()

        elif pick >= 2:
            use_item(user.Player["inv"][pick - 2])

    deco.clear_l(clear_all=1)


def item_add(_item, amount=1):
    _item["item_amount"] = amount
    for item in user.Player["inv"]:
        if _item["item_name"] == item["item_name"]:
            item["item_amount"] += amount
            return
    _item["item_amount"] = amount
    user.Player["inv"].append(copy.deepcopy(_item))


def use_item(item):
    if item["item_type"] in ["food", "potion"]:
        if user.check_hp():
            for i, k in item["player_affected_stats"].items():
                user.Player[i] += k
                user.check_hp_max()
            remove_item(item)

            deco.clear_l(s="", clear_all=1)

            deco.player_hud()

            article = "an" if item["item_name"].lower() in ["a", "e", "i", "o", "u"] else "a"
            print(f'You ate {article} {item["item_name"]}')
            show_item_effects(item, already_did=1)
        else:

            deco.clear_l(s="", clear_all=1)
            deco.player_hud()
            print("You are at full HP already.")

    else:
        deco.player_hud()
        print(f'You can\'t use the {item["item_name"]} right now...')


def remove_item(_item, amount=1):
    _item["item_amount"] -= amount
    if _item["item_amount"] <= 0:
        user.Player["inv"] = [item for item in user.Player["inv"] if item != _item]


def inv_inspect():
    inspecting = True
    while inspecting:
        deco.clear_l(s="", clear_all=1)
        deco.print_header("Inventory (Inspecting)")

        if len(user.Player["inv"]) <= 0:
            deco.clear_l()
            print("1. Stop inspecting")
            deco.clear_l()

        else:
            print("1. Stop inspecting")
            for i, item in enumerate(user.Player["inv"]):

                print(f'{i+2}. {item["item_name"]} {("x "+str(item["item_amount"])) if item["item_amount"]>1 else ""}')

        pick = user.user_input(len(user.Player["inv"]) + 1)

        if not pick:
            inspecting = False
            deco.clear_l(s="", clear_all=1)
            deco.player_hud()


        else:
            item_inspect(user.Player["inv"][pick - 1])


def item_inspect(item):
    deco.print_header(item["item_name"], 1)

    deco.print_in_line(item["item_desc"])
    show_item_effects(item)

    str(input("Press enter to close."))


def show_item_effects(item, already_did=0):

    if not already_did:
        for i, k in item["player_affected_stats"].items():
            if k > 0:
                if i == "hp":
                    print(f"{colors.green}It heals you for {k} HP{colors.reset}.")
                if i == "hp_max":
                    print(f"{colors.green}It increases your max HP by {k} HP{colors.reset}.")
                if i == "str":
                    print(f"{colors.red}It increases your strength by {k}{colors.reset}.")
                if i == "dex":
                    print(f"{colors.light_blue}It increases your dexterity by {k}{colors.reset}.")
                if i == "def":
                    print(f"{colors.light_blue}It increases your defense by {k}{colors.reset}.")
                if i == "xp":
                    print(f"{colors.green}It increases your xp by {k} points{colors.reset}.")
                if i == "lvl":
                    print(f"{colors.green}It increases your Level by {k} Level{colors.reset}.")
    else:
        for i, k in item["player_affected_stats"].items():
            if k > 0:
                if i == "hp":
                    print(f"{colors.green}It healed you for {k} HP{colors.reset}.")
                if i == "hp_max":
                    print(f"{colors.green}It increased your max HP by {k} HP{colors.reset}.")
                if i == "str":
                    print(f"{colors.red}It increased your strength by {k}{colors.reset}.")
                if i == "dex":
                    print(f"{colors.light_blue}It increased your dexterity by {k}{colors.reset}.")
                if i == "def":
                    print(f"{colors.light_blue}It increased your defense by {k}{colors.reset}.")
                if i == "xp":
                    print(f"{colors.green}It increased your xp by {k} points{colors.reset}.")
                if i == "lvl":
                    print(f"{colors.green}It increased your Level by {k} Level{colors.reset}.")