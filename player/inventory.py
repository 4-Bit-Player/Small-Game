from player import user, crafting
from decoration import deco, colors
import importlib
from recipies import armor, use_ables, weapons


def open_inventory():
    inv_open = True
    deco.clear_l(1, "")
    deco.player_hud()
    available_items = []
    show_items = "All"
    show_items_list = ["All", "Use-Ables", "Weapons", "Armor", "Materials"]
    items_list_index = 0
    while inv_open:

        deco.print_header("Inventory")

        if len(user.Player["inv"]) <= 0:

            print("Your inventory is currently empty.")
            print("1. Close inventory")
            print("2. Inspect item")
            print("3. Craft stuff")
            deco.clear_l()

            pick = user.user_input(3)
        else:
            print("1. Close inventory")
            print("2. Inspect item")
            print("3. Craft stuff")
            print("4. Cycle through All/Use-ables/Equip/Materials")
            deco.print_header(show_items, s="~")

            available_items = list_inventory(5, show_items)

            pick = user.user_input(len(available_items) + 5)

        if not pick:
            inv_open = False

        elif pick == 1:
            inv_inspect()

        elif pick == 2:
            inv_crafting()

        elif pick == 3:
            items_list_index = (items_list_index + 1) % len(show_items_list)
            show_items = show_items_list[items_list_index]
            deco.clear_l(1, "")
            deco.player_hud()

        elif pick >= 4:
            use_item(available_items[pick - 4])

    deco.clear_l(1, "")


def use_item(item):
    if item["item_type"] in ["food"]:
        if user.check_hp():
            for i, k in item["player_affected_stats"].items():
                user.Player[i] += k
                user.check_hp_max()
            crafting.remove_item(item)

            deco.clear_l(1, "")

            deco.player_hud()

            article = "an" if item["item_name"].lower() in ["a", "e", "i", "o", "u"] else "a"
            print(f'You ate {article} {item["item_name"]}')
            crafting.show_item_effects(item, already_did=1)
        else:

            deco.clear_l(1, "")
            deco.player_hud()
            print("You are at full HP already.")

    elif item["item_type"] in ["potion"]:
        healing = False
        for stat, amount in item["player_affected_stats"].items():
            if stat == "hp":
                if user.Player["hp"] >= user.Player["hp_max"]:
                    healing = True

        if not healing:
            for i, k in item["player_affected_stats"].items():
                user.Player[i] += k
                user.check_hp_max()
            crafting.remove_item(item)

            deco.clear_l(1, "")

            deco.player_hud()

            article = "an" if item["item_name"].lower() in ["a", "e", "i", "o", "u"] else "a"
            print(f'You used {article} {item["item_name"]}')
            crafting.show_item_effects(item, already_did=1)
        else:
            print("You are already at max hp.")

    elif item["item_type"] in ["equipment"]:
        user.equip_item(item)
        deco.clear_l(1, "")

        deco.player_hud()

    else:
        deco.clear_l(1, "")
        print(f'{colors.red}You can\'t use the {item["item_name"]} right now...{colors.reset}')


def inv_inspect():
    inspecting = True
    while inspecting:
        deco.print_header("Inventory (Inspecting)", 1)

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
            deco.clear_l(1, "")
            deco.player_hud()

        else:
            item_inspect(user.Player["inv"][pick - 1])


def item_inspect(item):
    deco.print_header(item["item_name"], 1)

    deco.print_in_line(item["item_desc"])
    if item["item_type"] in ["potion", "equipment", "food"]:
        crafting.show_item_effects(item)
    if item["item_type"] == "equipment":
        print(f'Upgrade slots used: {item["upgrades"][0]}/{item["upgrades"][1]}')
        print("Can be equipped")
    print()
    str(input("Press enter to close."))


def inv_crafting():
    active_crafting = True
    unlocked_recipies = []
    show_items = "All"
    show_items_list = ["All", "Use-Ables", "Weapons", "Armor"]
    items_list_index = 0

    package = importlib.import_module("recipies")
    module_names = package.__all__

    crafting_list = []
    for module_name in module_names:
        module = importlib.import_module(f"{'recipies'}.{module_name}")
        if hasattr(module, module_name):
            crafting_list.extend(getattr(module, module_name))

    for c_recipies in crafting_list:
        if c_recipies["req_lvl"] <= user.Player["lvl"]:
            unlocked_recipies.append(c_recipies)

    deco.clear_l(1, "")

    while active_crafting:
        deco.print_header("Craft Item")
        print("1. Stop Crafting")
        print("2. Cycle through All/Use-ables/Weapons/Armor")
        deco.print_header(show_items, s="~")
        option = 3

        shown_recipes = list_recipes(unlocked_recipies, show_items)

        for c_recipies in shown_recipes:
            print(f'{option}. {c_recipies["name"]}')
            requirements = []
            for req_items in c_recipies["req_res"]:
                if req_items:
                    for u_item in user.Player["inv"]:
                        if req_items == u_item["item_name"]:
                            if c_recipies["req_res"][req_items] <= u_item["item_amount"]:
                                requirements.append(f'{colors.green}{c_recipies["req_res"][req_items]}x {req_items}')
                                break

                    else:
                        requirements.append(f'{colors.red}{c_recipies["req_res"][req_items]}x {req_items}')
            if requirements:
                print(f'You need ' + ", ".join(requirements) + colors.reset)
            else:
                print()

            option += 1

        pick = user.user_input(len(shown_recipes)+2)

        if not pick:
            deco.clear_l(1, "")
            deco.player_hud()
            return

        elif pick == 1:
            items_list_index = (items_list_index + 1) % len(show_items_list)
            show_items = show_items_list[items_list_index]
            deco.clear_l(1, "")

        elif pick >= 2:
            # noinspection PyTypeChecker
            if shown_recipes[pick - 2]["type"] not in ["armor_list"]:
                crafting.craft(shown_recipes[pick - 2])
            else:
                crafting.craft_list(shown_recipes[pick - 2])


def list_inventory(start_number=1, item_type="All"):
    available_items = []
    show_text = []

    if item_type == "Use-Ables":
        allowed_items = ["potion", "food"]
    elif item_type == "Equipment":
        allowed_items = ["equipment"]
    elif item_type == "Materials":
        allowed_items = ["material", "item"]
    elif item_type == "Armor":
        allowed_items = ["armor"]

    else:
        allowed_items = ["material", "item", "equipment", "potion", "food", "armor"]

    for item in user.Player["inv"]:
        if item["item_type"] in allowed_items:
            equipped = ""
            upgraded = ""
            try:
                if item["equipped"] == 1:
                    equipped = "  (equipped)"
                if item["upgrades"][0] >= 1:
                    upgraded = " *"
            except KeyError:
                pass

            available_items.append(item)

            show_text.append(f'{item["item_name"]}{(" x "+str(item["item_amount"])) if item["item_amount"]>1 else""}'
                             f'{equipped}{upgraded}')

    for i, text in enumerate(show_text):
        print(f'{i+start_number}. {text}')

    return available_items


def list_recipes(c_recipes, item_type="All",):
    available_items = []
    if item_type == "Use-Ables":
        allowed_items = ["potion", "food"]
    elif item_type == "Weapons":
        allowed_items = ["equipment"]
    elif item_type == "Armor":
        allowed_items = ["armor", "armor_list"]
    elif item_type == "Materials":
        allowed_items = ["material", "item"]
    else:
        allowed_items = ["material", "item", "equipment", "potion", "food", "armor", "armor_list"]

    for item in c_recipes:
        if item["type"] in allowed_items:

            available_items.append(item)

    return available_items
