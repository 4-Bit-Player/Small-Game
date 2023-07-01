from player import user, crafting, recipes
from decoration import deco, colors


def open_inventory():
    inv_open = True
    deco.clear_l(1, "")
    deco.player_hud()

    while inv_open:

        deco.print_header("Inventory")

        if len(user.Player["inv"]) <= 0:

            print("Your inventory is currently empty.")
            print("1. Close inventory")
            print("2. Inspect item")
            print("3. Craft stuff")
            deco.clear_l()

            pick = user.user_input(len(user.Player["inv"]) + 3)
        else:
            print("1. Close inventory")
            print("2. Inspect item")
            print("3. Craft stuff")
            deco.print_header("Use/Equip Item")
            for i, item in enumerate(user.Player["inv"]):
                equipped = ""
                upgraded = ""
                try:
                    if item["equipped"] == 1:
                        equipped = "  (equipped)"
                    if item["upgrades"][0] >= 1:
                        upgraded = " *"
                except KeyError:
                    pass

                print(f'{i+4}. {item["item_name"]}{(" x "+str(item["item_amount"])) if item["item_amount"]>1 else ""}'
                      f'{equipped}{upgraded}')

            pick = user.user_input(len(user.Player["inv"]) + 3)

        if not pick:
            inv_open = False

        elif pick == 1:
            inv_inspect()

        elif pick == 2:
            inv_crafting()

        elif pick >= 3:
            use_item(user.Player["inv"][pick - 3])

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
        deco.clear_l(1, "")
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

    deco.clear_l(1, "")

    while active_crafting:
        deco.print_header("Craft Item")
        print("1. Stop Crafting")
        option = 2

        for c_recipies in recipes.recipies:
            if c_recipies["req_lvl"] <= user.Player["lvl"]:

                unlocked_recipies.append(c_recipies)

                print(f'{option}. {c_recipies["name"]}')
                requirements = []
                for req_items in c_recipies["req_res"]:
                    for u_item in user.Player["inv"]:
                        if req_items == u_item["item_name"]:
                            if c_recipies["req_res"][req_items] <= u_item["item_amount"]:
                                requirements.append(f'{colors.green}{c_recipies["req_res"][req_items]}x {req_items}')
                                break

                    else:
                        requirements.append(f'{colors.red}{c_recipies["req_res"][req_items]}x {req_items}')

                print(f'You need ' + ", ".join(requirements) + colors.reset)

                option += 1

        pick = user.user_input(len(unlocked_recipies)+1)

        if not pick:
            deco.clear_l(1, "")
            deco.player_hud()
            return
        elif pick >= 1:
            crafting.craft(unlocked_recipies[pick - 1])


