import time
from numbers import Number

from input_system import num_input, text_input
from player import user, u_KeyInput
from decoration import deco
from player.crafting import item_add
from printing import n_print

def cheat_menu():
    options = [
        ["What would you like to do?"],
        [deco.line_r("~")],
        "Return",
        "Change stats",
        "Reset Player",
        "Reset Everything",
        "Give Item",
    ]
    while True:
        pick = u_KeyInput.keyinput(options)
        if not pick:
            return
        if pick == 1:
            change_stats()
        elif pick == 2:
            if u_KeyInput.user_confirmation("reset the character"):
                user.restart()
        elif pick == 3:
            if u_KeyInput.user_confirmation("reset EVERYTHING"):
                pass
                #location_actions.restart()
        elif pick == 4:
            give_item()




def change_stats():
    options = [["index",1,0,0,0,0,0,0,0]]
    while True:
        changeable_stat = []
        options = [options[0],["What do you want to change?"], [deco.line_r("~")], "Return", [""]]
        for stat, val in user.Player.items():
            if not isinstance(val, Number):
                continue
            options.append(f"{stat}: {val}")
            changeable_stat.append(stat)

        pick = u_KeyInput.keyinput(options)
        if not pick:
            return
        change_that_stat(changeable_stat[pick-1])


def change_that_stat(stat):
    pick = num_input(f"Please enter a new value for the stat ({stat})\n(leave empty to return)\n\nCurrent Value: {user.Player[stat]}\nNew Value:",
                     whole_number=False,
                     escape_allowed=True)
    if pick is None:
        return
    user.Player[stat] = pick


def give_item():
    item_name = text_input("Enter the item name you want to get: ")
    if not item_name:
        return
    n_print()
    item_amount = num_input(f"How many do you want to get of {item_name}?\nAmount: ",
                            min_num=0, whole_number=True, escape_allowed=True)
    if item_amount is None or item_amount == 0:
        return
    if item_add(item_name, item_amount, False):
        n_print(f"{item_name} x {item_amount} added successfully")
    else:
        n_print("Wasn't able to give you the item.")
    time.sleep(1)
