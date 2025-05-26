from player import user, crafting, u_KeyInput
from decoration import deco, colors
from player.keyinput_index_class import KeyinputIndexClass
from printing.print_queue import n_print


def open_inventory():
    inv_open = True
    deco.clear_screen()
    available_items = []
    show_items = "All"
    show_items_list = ["All", "Use-Ables", "Weapons", "Armor", "Materials"]
    items_list_index = 0
    index = []
    overflow = []
    while inv_open:
        if index:
            a_selection = [index]
        else:
            a_selection: list = []

        if len(user.Player["inv"]) == 0:
            a_selection.append([1, "Close inventory",
                                "Inspect item", "Craft stuff",
                                "Cycle through All/Use-ables/Weapons/Armor/Materials"])
            a_selection.append([deco.line_r()])
            a_selection.append(["Your inventory is currently empty.", ""])

        else:
            a_selection.append([1, "Close inventory",
                                "Inspect item", "Craft stuff",
                                "Cycle through All/Use-ables/Weapons/Armor/Materials"])
            a_selection.append([deco.print_header_r(show_items, s="~")])
            for item in show_inventory(show_items):
                a_selection.append(item)

            available_items = list_inventory(5, show_items)
        if overflow:
            overflow.insert(0, " ")
            a_selection.append(overflow)
            overflow = []

        pick = u_KeyInput.keyinput(a_selection, header="Inventory", hud=True)

        if not pick:
            inv_open = False

        elif pick == 1:
            inv_inspect()

        elif pick == 2:
            inv_crafting()

        elif pick == 3:
            items_list_index = (items_list_index + 1) % len(show_items_list)
            show_items = show_items_list[items_list_index]

        elif pick >= 4:
            overflow = use_item(available_items[pick - 4])

        if isinstance(a_selection[0], KeyinputIndexClass):
            index = a_selection[0]
    deco.clear_screen()


def use_item(item):
    overflow = []
    if item["item_type"] in ["food"]:
        if user.check_hp():
            for i, k in item["player_affected_stats"].items():
                user.Player[i] += k
                user.check_hp_max()
            crafting.remove_item(item)

            article = "an" if item["item_name"].lower() in ["a", "e", "i", "o", "u"] else "a"
            overflow.append(f'You ate {article} {item["item_name"]}')
            overflow += (crafting.show_item_effects(item, already_did=1))

        else:
            return [colors.red +"You are at full HP already."+colors.reset]

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

            article = "an" if item["item_name"].lower() in ["a", "e", "i", "o", "u"] else "a"
            for i in crafting.show_item_effects(item, already_did=1):
                overflow.append(i)
            overflow.append(f'You used {article} {item["item_name"]}')

        else:
            overflow.append("You are already at max hp.")

    elif item["item_type"] in ["equipment", "armor"]:
        user.equip_item(item)

    else:
        overflow.append(f'{colors.red}You can\'t use the {item["item_name"]} right now...{colors.reset}')
    return overflow


def inv_inspect():
    inspecting = True
    index = []
    while inspecting:
        show = [["", deco.print_header_r("Inventory (Inspecting)")]]
        if index:
            show.insert(0, index)

        if len(user.Player["inv"]) <= 0:
            show.append([deco.line_r()])
            show.append("Stop inspecting")
            show.append([deco.line_r()])

        else:
            show.append("Stop inspecting")
            show.append([deco.line_r("~")])
            for item in user.Player["inv"]:

                show.append(f'{item["item_name"]} {("x "+str(item["item_amount"])) if item["item_amount"]>1 else ""}')

        pick = u_KeyInput.keyinput(show)
        if not pick:
            inspecting = False

        else:
            item_inspect(user.Player["inv"][pick - 1])

        if isinstance(show[0], KeyinputIndexClass):
            index = show[0]


def item_inspect(item):
    out = deco.print_header_r(item["item_name"]) + "\n" + deco.format_text_in_line([item["item_desc"]]) + "\n"

    if item["item_type"] in ["potion", "equipment", "food", "armor"]:
        for i in crafting.show_item_effects(item):
            out += i + "\n"
    if item["item_type"] in ["equipment", "armor"]:
        out += f'Upgrade slots used: {item["upgrades"][0]}/{item["upgrades"][1]}\n"Can be equipped"'
    out += ("\nPress enter to close.\n")
    n_print(out)
    u_KeyInput.wait_for_keypress()


def inv_crafting():
    active_crafting = True
    unlocked_recipies = []
    show_items = "All"
    show_items_list = ["All", "Use-Ables", "Weapons", "Armor"]
    items_list_index = 0


    for c_recipies in crafting._all_crafting_recipes.values():
        if c_recipies["req_lvl"] <= user.Player["lvl"]:
            unlocked_recipies.append(c_recipies)
    overflow = []
    show = []
    while active_crafting:
        show += [
            [deco.print_header_r("Craft Item")],
            "Stop Crafting",
            "Cycle through All/Use-ables/Weapons/Armor",
            [deco.print_header_r(show_items, s="~")]]

        shown_recipes = list_recipes(unlocked_recipies, show_items)

        for c_recipies in shown_recipes:
            show.append(f'{c_recipies["name"]}')
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
                show.append([f'   You need ' + ", ".join(requirements) + colors.reset])
            else:
                show.append([""])
        if overflow:
            show.append(overflow)
            overflow = ""
        pick = u_KeyInput.keyinput(show)
        if not pick:
            return

        elif pick == 1:
            items_list_index = (items_list_index + 1) % len(show_items_list)
            show_items = show_items_list[items_list_index]

        elif pick >= 2:
            # noinspection PyTypeChecker
            if shown_recipes[pick - 2]["type"] not in ["armor_list"]:
                overflow = crafting.craft(shown_recipes[pick - 2])
            else:
                crafting.craft_list(shown_recipes[pick - 2])

        if isinstance(show[0], KeyinputIndexClass):
            show = [show[0]]


def list_inventory(start_number=1, item_type="All"):
    available_items = []
    show_text = []

    if item_type == "Use-Ables":
        allowed_items = ["potion", "food"]
    elif item_type in ["Equipment", "Weapons"]:
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
                             f'{upgraded}{equipped}')

    #for i, text in enumerate(show_text):
    #    print(f'{i+start_number}. {text}')

    return available_items


def show_inventory(item_type="All"):
    available_items = []
    show_text = []

    if item_type == "Use-Ables":
        allowed_items = ["potion", "food"]
    elif item_type in ["Equipment", "Weapons"]:
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
                             f'{upgraded}{equipped}')

    return show_text


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
