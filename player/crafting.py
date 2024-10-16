from player import user, u_KeyInput
from decoration import colors, deco
from copy import deepcopy
from items import items, potions, food, materials, equipment, armor
from printing.print_queue import n_print
import recipies.weapons as r_weapons
import recipies.armor as r_armor
import recipies.use_ables as r_use_ables

all_items = {}
all_crafting_recipes = {}

def item_init():
    global all_items
    global all_crafting_recipes
    for item_list in [items.items, potions.potions, materials.materials, armor.armor, equipment.equipment, food.food]:
        for item in item_list:
            all_items[item["item_name"]] = item
    for item_list in [r_armor.armor, r_use_ables.use_ables, r_weapons.weapons,]:
        for item in item_list:
            all_crafting_recipes[item["name"]] = item


def craft(recipe):

    if crafting_check(recipe):
        for item, quantity in recipe["req_res"].items():
            for u_item in user.Player["inv"]:
                if item == u_item["item_name"]:
                    remove_item(u_item, quantity)

        item_add(recipe["result"], recipe["re_amount"])

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
    user.Player["inv"].remove(_item)


def item_add(item_name, amount=1, apology=True) -> bool:
    for item in user.Player["inv"]:
        if item["item_name"] == item_name:
            item["item_amount"] += amount
            return True
    n_item = item_search(item_name, apology)
    if n_item is None:
        return False
    n_item["item_amount"] = amount
    user.Player["inv"].append(n_item)
    return True


def item_search(item_name, apology=True) -> dict | None:
    if item_name in all_items:
        return deepcopy(all_items[item_name])
    if not apology:
        n_print(f"Failed to find {item_name}...\n"
                f"(Press enter to continue)")
        u_KeyInput.wait_for_keypress()
        deco.clear_screen(6)
        return None
    n_print(deco.line_r() + f'\nLooking up the item "{item_name}" was not successful... :(\n'
    "Please write me where you got this error, so I can fix it.\n"
    "Additionally you'll get a written apology. \nYou can sell that at a merchant for a bit of money.\n"
    "(Press enter to continue)")
    u_KeyInput.wait_for_keypress()
    deco.clear_screen(6)
    item_add("An apology from the dev :(", 1, False)
    return None


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
                deco.clear_screen()
                return

            upgrade_equipment(item_list[pick-1])

        else:
            n_print("You have nothing to upgrade right now.\n"+ deco.line_r() + "\nDo something else...\n")
            u_KeyInput.wait_for_keypress()
            working = False


def upgrade_equipment(equip_to_upgrade):
    up_equipment = 1
    deco.clear_screen()
    while up_equipment:
        header = (deco.line_r() + "\n" +
                  f'Upgrading {equip_to_upgrade["item_name"]} '
                  f'{equip_to_upgrade["upgrades"][0]}/{equip_to_upgrade["upgrades"][1]}\n' +
                  deco.line_r()
                  )

        if equip_to_upgrade["upgrades"][0] >= equip_to_upgrade["upgrades"][1]:
            n_print(
                header+"\n"
                "You can't upgrade this item anymore.\n" +
                deco.line_r() +
                "\nContinue\n"
                )
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
            n_print(
                header + "\n"
                "You don't have any material for upgrading this weapon.\n"
            )
            u_KeyInput.wait_for_keypress()
            pick = 0
        else:
            pick = u_KeyInput.keyinput(options, header)

        if not pick:
            deco.clear_screen()
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
        equip_to_upgrade = upgraded_item
        n_print(
            deco.line_r() + "\n"
            f'{colors.green}Successfully upgraded the {upgraded_item["item_name"]}{colors.reset}\n' +
            deco.line_r() + "\n"
        )


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
        elif i == "def_multi":
            overflow.append(f"{colors.light_blue}It {word_time} your defense multiplier by {k} %{colors.reset}.")
        elif i == "xp":
            overflow.append(f"{colors.green}It {word_time} your xp by {k} points{colors.reset}.")
        elif i == "lvl":
            overflow.append(f"{colors.green}It {word_time} your Level by {k} Level{colors.reset}.")
    return overflow


def show_item_effects_r(item, already_did=0):
    word_time = 'increases' if not already_did else 'increased'
    out = ""
    for i, k in item["player_affected_stats"].items():
        if k > 0:
            if i == "hp":
                out += f"{colors.green}It heal{'s' if not already_did else 'ed'} you for {k} HP{colors.reset}.\n"
            elif i == "hp_max":
                out += f"{colors.green}It {word_time} your max HP by {k} HP{colors.reset}."
            elif i == "str":
                out += f"{colors.red}It {word_time} your strength by {k}{colors.reset}."
            elif i == "str_base":
                out += f"{colors.red}It {word_time} your base strength by {k}{colors.reset}."
            elif i == "dex":
                out += f"{colors.light_blue}It {word_time} your dexterity by {k}{colors.reset}."
            elif i == "def":
                out += f"{colors.light_blue}It {word_time} your defense by {k}{colors.reset}."
            elif i == "def_base":
                out += f"{colors.light_blue}It {word_time} your base defense by {k}{colors.reset}."
            elif i == "xp":
                out += f"{colors.green}It {word_time} your xp by {k} points{colors.reset}."
            elif i == "lvl":
                out += f"{colors.green}It {word_time} your Level by {k} Level{colors.reset}."
    return out


def craft_list(c_list):

    deco.clear_screen()
    overflow = []
    selection = []
    while colors:
        selection += [
            [deco.print_header_r(c_list["name"])],
            "Back",
            [deco.line_r("~")]
        ]

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
        deco.clear_screen()

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
