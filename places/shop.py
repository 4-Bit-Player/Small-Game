import random
from player import user, crafting, inventory, u_KeyInput
from decoration import deco, colors


def buy(item):
    if isinstance(item["name"], list):
        item_name = random.choice(item["name"])

    else:
        item_name = item["name"]
    article = "an " if item_name[0].lower() in ["a", "e", "i", "o", "u"] else "a "
    article = article if item_name[-1] not in ["s", "c", "i"] else ""

    if check_money(item["price"]):
        crafting.item_add(item["item"])
        out = f'\n{colors.green}You bought {article}{item_name}{colors.reset}'
    else:
        if isinstance(item["name"], list):
            item_name = item["name"][0]
            article = "an " if item_name[0].lower() in ["a", "e", "i", "o", "u"] else "a "
            article = article if item_name[-1] not in ["s", "c", "i"] else ""
        out = f'\n{colors.red}You don\'t have enough money to buy {article}{item_name} right now.{colors.reset}'

    return out


def check_money(price):
    if user.Player["gold"] >= price:
        user.Player["gold"] -= price
        return True
    else:
        return False


def shop_sell():
    selling = 1
    sell_all = False

    overflow = ""
    while selling:
        out = [1, "Back", "Toggle sell one/all"]
        av_items = inventory.show_inventory()
        av_items.insert(0,1)
        options = [[deco.line_r()], out, [deco.print_header_r("Sell one" if not sell_all else "Sell all")], av_items]
        item_list = inventory.list_inventory()
        if overflow:
            options.append([overflow])
            overflow = ""
        pick = u_KeyInput.keyinput(options, hud=True)

        if not pick:
            deco.clear_screen()
            return

        if pick == 1:
            sell_all = not sell_all

        else:
            if sell_all:
                overflow = sell_item(item_list[pick-2], item_list[pick-2]["item_amount"])

            else:
                overflow = sell_item(item_list[pick - 2])


def sell_item(item, amount=1):
    if not "sell_price" in item:
        return "\nYou can't sell this Item.\n"

    user.Player["gold"] += item["sell_price"] * amount
    crafting.remove_item(item, amount)
    return (f'\n{colors.green}Sold {amount}x {item["item_name"]} for {colors.gold}{item["sell_price"] * amount} '
          f'Gold{colors.reset}\n')

