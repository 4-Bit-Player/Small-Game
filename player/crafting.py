from player import user, u_KeyInput
from decoration import colors, deco
from copy import deepcopy
from items import items, potions, food, materials, equipment, armor
import importlib

all_items = {}


def item_init():
    global all_items
    for item_list in [items.items, potions.potions, materials.materials, armor.armor, equipment.equipment, food.food]:
        for item in item_list:
            all_items[item["item_name"]] = item


def craft(recipe):

    if crafting_check(recipe):
        for item, quantity in recipe["req_res"].items():
            for u_item in user.Player["inv"]:
                if item == u_item["item_name"]:
                    remove_item(u_item, quantity)

        item_add(recipe["result"], recipe["re_amount"], recipe["type"])

        return [f'{colors.green}You crafted {recipe["re_amount"]}x {recipe["name"]}.{colors.reset}']
    else:
        return [f"{colors.red}You don't have all Materials{colors.reset}"]


def crafting_check(recipe):
    for item, quantity in recipe["req_res"].items():
        found = False
        for u_item in user.Player["inv"]:
            if item == u_item["item_name"]:
                if u_item["item_amount"] >= quantity:
                    found = True
                    break

        if not found:
            return False

    return True


def remove_item(_item, amount=1):
    _item["item_amount"] -= amount
    if _item["item_amount"] > 0:
        return
    if _item["item_type"] == "equipment":
        if _item["equipped"]:
            user.equip_item(_item)

    user.Player["inv"] = [item for item in user.Player["inv"] if item != _item]


def item_add(item_name, amount=1, search_in="All"):
    _item = item_search(item_name, search_in)
    for item in user.Player["inv"]:
        if item["item_name"] == item_name:
            item["item_amount"] += amount
            return
    n_item = deepcopy(_item)
    n_item["item_amount"] = amount
    user.Player["inv"].append(n_item)


def item_search(item_name, search_in="All"):
    if item_name in all_items:
        return all_items[item_name]
    if search_in in ["potion", "item", "material"]:
        search_in = search_in + "s"

    if search_in != "All":
        package = importlib.import_module("items")
        module_names = package.__all__
        found_lists = []

        for module_name in module_names:
            module = importlib.import_module(f"{'items'}.{module_name}")
            if hasattr(module, search_in):
                found_lists.extend(getattr(module, search_in))

        for item in found_lists:
            if item["item_name"] == item_name:
                return item

    else:
        for item_list in [items.items, potions.potions, materials.materials, armor.armor, equipment.equipment, food.food]:
            for item in item_list:
                if item["item_name"] == item_name:
                    return item

    deco.clear_l(1)

    print(f'Looking up the item "{item_name}" was not successful...')
    print("Fuck")

    str(input("Press enter to crash the program. :)"))


def available_equipment_list():
    item_list = []
    for item in user.Player["inv"]:
        if item["item_type"] in ["equipment", "armor"]:
            item_list.append(item)

    return item_list


def upgrading():
    working = True

    while working:
        item_list = available_equipment_list()
        if item_list:
            options = [
                f"Don't upgrade anything.",
                [deco.line_r("~")],
            ]
            for item in item_list:
                av_upgrades = f'{item["upgrades"][0]}/{item["upgrades"][1]}'
                item_text = f'{item["item_name"]} {av_upgrades}'
                eq = "(equipped)" if item["equipped"] else ""

                if item["upgrades"][0] >= item["upgrades"][1]:
                    item_text = f'{colors.red}{item_text}{colors.reset}'

                options.append(item_text +
                               f'{(" x "+str(item["item_amount"])) if item["item_amount"]>1 else ""} {eq}')

            pick = u_KeyInput.keyinput(options, "Upgrading Equipment")

            if not pick:
                deco.clear_l(1, "")
                return

            upgrade_equipment(item_list[pick-1])

        else:
            print("You have nothing to upgrade right now.")
            deco.clear_l()
            print("Do something else...")
            deco.clear_l(1, "")
            u_KeyInput.wait_for_keypress()
            working = False


def upgrade_equipment(equip_to_upgrade):
    up_equipment = 1
    deco.clear_l(1, "")
    while up_equipment:
        header = (deco.line_r() + "\n" +
                  f'Upgrading {equip_to_upgrade["item_name"]} '
                  f'{equip_to_upgrade["upgrades"][0]}/{equip_to_upgrade["upgrades"][1]}\n' +
                  deco.line_r()
                  )

        if equip_to_upgrade["upgrades"][0] >= equip_to_upgrade["upgrades"][1]:
            print(header)
            print("You can't upgrade this item anymore.")
            deco.clear_l()
            print("Continue")
            u_KeyInput.wait_for_keypress()
            return
        options = ["Don't upgrade anything."]
        available_material = []
        for item in user.Player["inv"]:
            if item["item_type"] == "item":
                if equip_to_upgrade["player_slot"] in item["compatible_slots"]:
                    options.append(item["item_name"])
                    options.append(show_item_effects(item))
                    available_material.append(item)
        if not available_material:
            print(header)
            print("You don't have any material for upgrading this weapon.")
            u_KeyInput.wait_for_keypress()
            pick = 0
        else:
            pick = u_KeyInput.keyinput(options, header)

        if not pick:
            deco.clear_l(1, "")
            return

        used_item = available_material[pick - 1]

        upgraded_item = deepcopy(equip_to_upgrade)
        upgraded_item["item_amount"] = 1

        if equip_to_upgrade["equipped"]:
            user.equip_item(equip_to_upgrade)

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
            if item["item_name"] == upgraded_item["item_name"] and \
                    item["player_affected_stats"] == upgraded_item["player_affected_stats"] and \
                    item["upgrades"] == upgraded_item["upgrades"]:

                item["item_amount"] += 1
                added += 1
                break

        if not added:
            user.Player["inv"].append(upgraded_item)

        if upgraded_item["equipped"]:
            user.equip_item(upgraded_item)

        deco.clear_l(1)
        print(f'{colors.green}Successfully upgraded the {upgraded_item["item_name"]}{colors.reset}')
        deco.clear_l()
        equip_to_upgrade = upgraded_item


def show_item_effects(item, already_did=0):
    overflow = []
    for i, k in item["player_affected_stats"].items():
        word_time = 'increases' if not already_did else 'increased'

        if k < 0:
            word_time = "de" + word_time[2:]
            k = abs(k)
        if i == "hp":
            overflow.append(f"{colors.green}It heal{'s' if not already_did else 'ed'} you for {k} HP{colors.reset}.")
        elif i == "hp_max":
            overflow.append(f"{colors.green}It {word_time} your max HP by {k} HP{colors.reset}.")
        elif i == "str":
            overflow.append(f"{colors.red}It {word_time} your strength by {k}{colors.reset}.")
        elif i == "str_base":
            overflow.append(f"{colors.red}It {word_time} your base strength by {k}{colors.reset}.")
        elif i == "dex":
            overflow.append(f"{colors.light_blue}It {word_time} your dexterity by {k}{colors.reset}.")
        elif i == "def":
            overflow.append(f"{colors.light_blue}It {word_time} your defense by {k}{colors.reset}.")
        elif i == "def_base":
            overflow.append(f"{colors.light_blue}It {word_time} your base defense by {k}{colors.reset}.")
        elif i == "xp":
            overflow.append(f"{colors.green}It {word_time} your xp by {k} points{colors.reset}.")
        elif i == "lvl":
            overflow.append(f"{colors.green}It {word_time} your Level by {k} Level{colors.reset}.")
    return overflow


def show_item_effects_r(item, already_did=0):
    word_time = 'increases' if not already_did else 'increased'

    for i, k in item["player_affected_stats"].items():
        if k > 0:
            if i == "hp":
                return f"{colors.green}It heal{'s' if not already_did else 'ed'} you for {k} HP{colors.reset}."
            elif i == "hp_max":
                return f"{colors.green}It {word_time} your max HP by {k} HP{colors.reset}."
            elif i == "str":
                return f"{colors.red}It {word_time} your strength by {k}{colors.reset}."
            elif i == "str_base":
                return f"{colors.red}It {word_time} your base strength by {k}{colors.reset}."
            elif i == "dex":
                return f"{colors.light_blue}It {word_time} your dexterity by {k}{colors.reset}."
            elif i == "def":
                return f"{colors.light_blue}It {word_time} your defense by {k}{colors.reset}."
            elif i == "def_base":
                return f"{colors.light_blue}It {word_time} your base defense by {k}{colors.reset}."
            elif i == "xp":
                return f"{colors.green}It {word_time} your xp by {k} points{colors.reset}."
            elif i == "lvl":
                return f"{colors.green}It {word_time} your Level by {k} Level{colors.reset}."


def craft_list(c_list):

    deco.clear_l(1, "")
    overflow = []
    selection = []
    while colors:
        deco.clear_l()
        selection += [
            [deco.line_r("~")],
            "Back",
            [deco.line_r("~")]
        ]

        deco.print_header(c_list["name"])
        for c_recipies in c_list["parts"]:
            selection.append(f'{c_recipies["name"]}')
            requirements = []
            if user.Player["lvl"] < c_recipies["req_lvl"]:
                selection.append([f'   {colors.red}'
                                  f'You have to be lvl {c_recipies["req_lvl"]} to craft this item{colors.reset}'])
            else:
                for req_items in c_recipies["req_res"]:
                    if req_items:
                        for u_item in user.Player["inv"]:
                            if req_items == u_item["item_name"]:
                                if c_recipies["req_res"][req_items] <= u_item["item_amount"]:
                                    requirements.append(f'{colors.green}'
                                                        f'{c_recipies["req_res"][req_items]}x {req_items}')
                                    break

                        else:
                            requirements.append(f'{colors.red}{c_recipies["req_res"][req_items]}x {req_items}')
                if requirements:
                    selection.append([f'   You need ' + ", ".join(requirements) + colors.reset])
                else:
                    selection.append([""])
        if overflow:
            selection.append(overflow)
        pick = u_KeyInput.keyinput(selection)
        deco.clear_l(1, "")

        if not pick:
            return

        if user.Player["lvl"] >= c_list["parts"][pick-1]["req_lvl"]:
            overflow = craft(c_list["parts"][pick-1])
        else:
            overflow = ([f'{colors.red}You have to be level {c_list["parts"][pick-1]["req_lvl"]} to craft this '
                        f'item.{colors.reset}'])

        if selection[0][0] == "index":
            selection = [selection[0]]
        else:
            selection = []
