from player import user
from decoration import colors, deco
import copy
from items import items, potions, food, materials, equipment


def available_crafting_list():
    item_list = []
    for item in user.Player["inv"]:
        if item["item_type"] == "equipment":
            item_list.append(item)

    return item_list


def craft(recipe):
    if crafting_check(recipe):
        for item, quantity in recipe["req_res"].items():
            for u_item in user.Player["inv"]:
                if item == u_item["item_name"]:
                    remove_item(u_item, quantity)

        recipe_item = item_search(recipe["result"])
        item_add(recipe_item, recipe["re_amount"])

        deco.clear_l(1)
        print(f'{colors.green}You crafted {recipe["re_amount"]}x {recipe["name"]}.{colors.reset}')
    else:
        deco.clear_l(1)
        print(f"{colors.red}You don't have all Materials{colors.reset}")


def crafting_check(recipe):
    for item, quantity in recipe["req_res"].items():
        found = False
        for u_item in user.Player["inv"]:
            if item == u_item["item_name"]:
                if u_item["item_amount"] >= quantity:
                    found = True

            if found:
                break

        if not found:
            return False

    return True


def remove_item(_item, amount=1):
    _item["item_amount"] -= amount
    if _item["item_amount"] <= 0:
        if _item["item_type"] == "equipment":
            user.equip_item(_item)

        user.Player["inv"] = [item for item in user.Player["inv"] if item != _item]


def item_add(_item, amount=1):
    for item in user.Player["inv"]:
        if _item["item_name"] == item["item_name"]:
            item["item_amount"] += amount
            return
    _item["item_amount"] = amount
    user.Player["inv"].append(copy.deepcopy(_item))


def item_search(item_name):

    for item in items.items:
        if item["item_name"] == item_name:
            return item

    for item in potions.potions:
        if item["item_name"] == item_name:
            return item

    for item in materials.materials:
        if item["item_name"] == item_name:
            return item

    for item in food.food:
        if item["item_name"] == item_name:
            return item

    for item in equipment.equipment:
        if item["item_name"] == item_name:
            return item

    deco.clear_l(1)

    print(f'Looking up the item "{item_name}" was not successful...')
    print("Fuck")

    str(input("Press enter to crash the program. :)"))


def upgrading():
    working = True

    while working:
        deco.clear_l(1)
        options = 1
        item_list = available_crafting_list()
        if item_list:

            print(f"{options}. Don't upgrade anything.")
            deco.clear_l(s="~")

            for item in item_list:
                options += 1

                av_upgrades = f'{item["upgrades"][0]}/{item["upgrades"][1]}'

                if item["upgrades"][0] >= item["upgrades"][1]:
                    print(f'{options}. {colors.red}{item["item_name"]} {av_upgrades} {colors.reset}'
                          f'{("x " + str(item["item_amount"])) if item["item_amount"] > 1 else ""} *')

                elif item["upgrades"][0] >= 1:
                    print(f'{options}. {item["item_name"]} {av_upgrades} '
                          f'{("x "+str(item["item_amount"])) if item["item_amount"]>1 else ""} *')

                else:
                    print(f'{options}. {item["item_name"]} {av_upgrades} '
                          f' {("x "+str(item["item_amount"])) if item["item_amount"]>1 else ""}')

            deco.clear_l()
            pick = user.user_input(len(item_list) + 1)

            if not pick:
                return

            upgrade_equipment(item_list[pick-1])

        else:
            print("You have nothing to upgrade right now.")
            deco.clear_l()
            str(input("Do something else..."))
            deco.clear_l(1, "")
            working = False


def upgrade_equipment(equip_to_upgrade):
    if equip_to_upgrade["upgrades"][0] >= equip_to_upgrade["upgrades"][1]:
        print("You can't upgrade this item anymore.")
        return

    available_material = []
    option = 1
    print("1. Don't upgrade it.")

    for item in user.Player["inv"]:
        if item["item_type"] == "item":
            if equip_to_upgrade["player_slot"] in item["compatible_slots"]:
                option += 1
                print(f'{option}. {item["item_name"]}')
                show_item_effects(item)
                available_material.append(item)

    pick = user.user_input(len(available_material) + 1)

    if not pick:
        return

    used_item = available_material[pick - 1]

    upgraded_item = copy.deepcopy(equip_to_upgrade)
    upgraded_item["item_amount"] = 1

    remove_item(equip_to_upgrade)

    # noinspection PyTypeChecker
    for stat, amount in used_item["player_affected_stats"].items():
        if stat in upgraded_item["player_affected_stats"]:
            upgraded_item["player_affected_stats"][stat] += amount

        else:
            upgraded_item["player_affected_stats"][stat] = amount

    remove_item(used_item)
    upgraded_item["upgrades"][0] += 1
    added = 0
    for item in user.Player["inv"]:
        if item == upgraded_item:
            item["item_amount"] += 1
            added += 1
            break

    if not added:
        user.Player["inv"].append(upgraded_item)

    deco.clear_l(1)
    print(f'{colors.green}Successfully upgraded the {upgraded_item["item_name"]}{colors.reset}')
    deco.clear_l()


def show_item_effects(item, already_did=0):
    word_time = 'increases' if not already_did else 'increased'

    for i, k in item["player_affected_stats"].items():
        if k > 0:
            if i == "hp":
                print(f"{colors.green}It heal{'s' if not already_did else 'ed'} you for {k} HP{colors.reset}.")
            elif i == "hp_max":
                print(f"{colors.green}It {word_time} your max HP by {k} HP{colors.reset}.")
            elif i == "str":
                print(f"{colors.red}It {word_time} your strength by {k}{colors.reset}.")
            elif i == "str_base":
                print(f"{colors.red}It {word_time} your base strength by {k}{colors.reset}.")
            elif i == "dex":
                print(f"{colors.light_blue}It {word_time} your dexterity by {k}{colors.reset}.")
            elif i == "def":
                print(f"{colors.light_blue}It {word_time} your defense by {k}{colors.reset}.")
            elif i == "def_base":
                print(f"{colors.light_blue}It {word_time} your base defense by {k}{colors.reset}.")
            elif i == "xp":
                print(f"{colors.green}It {word_time} your xp by {k} points{colors.reset}.")
            elif i == "lvl":
                print(f"{colors.green}It {word_time} your Level by {k} Level{colors.reset}.")
