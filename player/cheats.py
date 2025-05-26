import time
from numbers import Number
from player import user, u_KeyInput
from decoration import deco
from player.crafting import item_add
from player.terminal_funcs import pause_keyboard_input, resume_keyboard_input
from printing.print_queue import n_print, TemporaryDisablePrintUpdates
#from places.location_actions import restart

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
    pause_keyboard_input()
    n_print(f"Please enter a new value for the stat ({stat})\n(leave empty to return)\n\nCurrent Value: {user.Player[stat]}\nNew Value:")
    with TemporaryDisablePrintUpdates() as _:
        pick = input()
        resume_keyboard_input()
        if pick == "":
            return
        try:
            val = float(pick)
            user.Player[stat] = val
        except ValueError:
            return


def give_item():
    out = "Enter the item name you want to get: "
    pause_keyboard_input()
    n_print(out)
    with TemporaryDisablePrintUpdates() as _:
        item_name = input()
        if not item_name:
            resume_keyboard_input()
            return
        n_print(f"How many do you want to get of {item_name}?\nAmount: ")
        item_amount = input()
        resume_keyboard_input()
        if not item_amount:
            return
        try:
            item_amount = int(item_amount)
        except ValueError:
            return
        if item_add(item_name, item_amount, False):
            n_print(f"{item_name} x {item_amount} added successfully")
            time.sleep(1)