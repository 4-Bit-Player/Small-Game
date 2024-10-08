from numbers import Number
from player import user, u_KeyInput
from decoration import deco
from printing.print_queue import n_print
from places import location_actions

def cheat_menu():
    options = [
        ["What would you like to do?"],
        [deco.line_r("~")],
        "Return",
        "Change stats",
        "Reset Player",
        "Reset Everything"
    ]
    while True:
        pick = u_KeyInput.keyinput(options)
        if not pick:
            return
        if pick == 1:
            change_stats()
        if pick == 2:
            if u_KeyInput.user_confirmation("reset the character"):
                user.restart()
        if pick == 3:
            if u_KeyInput.user_confirmation("reset EVERYTHING"):
                location_actions.restart()




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
    n_print(f"Please enter a new value for the stat ({stat})\n(leave empty to return)\n\nCurrent Value: {user.Player[stat]}\nNew Value:")
    pick = input()
    if pick == "":
        return
    try:
        val = float(pick)
        user.Player[stat] = val
    except ValueError:
        return