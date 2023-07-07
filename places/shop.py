from player import user, crafting, inventory
from decoration import deco, colors


def buy(item):

    if check_money(item["price"]):

        r_item = crafting.item_search(item["item"])
        crafting.item_add(r_item)

        if isinstance(item["name"], list):
            pick = int(user.random_pick_list(item["name"]))

            item_name = item["name"][pick]

        else:
            item_name = item["name"]
        article = "an" if item_name.lower() in ["a", "e", "i", "o", "u"] else "a"
        deco.clear_l(1, "")
        print(f'You bought {article} {item_name}')
    else:
        deco.clear_l(1, "")
        if isinstance(item["name"], list):
            pick = int(user.random_pick_list(item["name"]))
            item_name = item["name"][pick]

        else:
            item_name = item["name"]
        article = "an" if item_name.lower() in ["a", "e", "i", "o", "u"] else "a"

        deco.clear_l()
        print(f'{colors.red}You don\'t have enough money to buy {article} {item_name} right now.{colors.reset}')
        deco.clear_l()
    return


def check_money(price):
    if user.Player["gold"] >= price:
        user.Player["gold"] -= price
        return True
    else:
        return False


def shop_sell():
    selling = 1
    options = ["Back", "Toggle sell one/all"]
    sell_all = False

    deco.clear_l(1)

    while selling:
        for number, option in enumerate(options):
            print(f'{number + 1}. {option}')

        deco.print_header("Sell one" if not sell_all else "Sell all")

        item_list = inventory.list_inventory(3)
        pick = user.user_input(len(options)+len(item_list))

        if not pick:
            deco.clear_l(1, "")
            break

        if pick == 1:
            sell_all = not sell_all
            deco.clear_l(1)

        else:
            if sell_all:
                deco.clear_l(1)
                sell_item(item_list[pick-2], item_list[pick-2]["item_amount"])
                deco.clear_l()

            else:
                deco.clear_l(1)
                sell_item(item_list[pick - 2])
                deco.clear_l()


def sell_item(item, amount=1):
    try:
        user.Player["gold"] += item["sell_price"] * amount
        crafting.remove_item(item, amount)
        print(f'{colors.green}Sold {amount}x {item["item_name"]} for {colors.gold}{item["sell_price"] * amount} '
              f'Gold{colors.reset}')

    except KeyError:
        print("You can't sell this Item.")
