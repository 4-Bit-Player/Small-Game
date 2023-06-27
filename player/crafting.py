from player import user
from decoration import colors, deco
import copy
from items import items, potions, food, materials, equipment


def available_crafting_list():
    pass


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

