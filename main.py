# To do:
"""
    Making everything moar beautiful
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    More locations
    more shops
    more items
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Ask Surly about character
    moar Equipment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    At some point:
    changing input, so you can navigate using text
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Add NPCs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Added/Changed:
    Added/changed Input system (it now also doesn't flash anymore)
    Quests
    more recipies (and also switching to selection)
    Working inventory system
    Saves work + completely revamped
    Printing completely changed, allowing centering
    Improved Crafting inventory
    upgrading of equipment
    possible to sell stuff
    moar Equipment
 """

import time
from decoration import story, deco, colors
from places.location_data import get_location, unlocks_init, location_init
from player import user, crafting, u_KeyInput, terminal_funcs
from places import show_location_actions, location_actions, quests
from printing import init_print
from printing.print_queue import n_print
from save_system.save_logic import save_check, save_update_score, highscore_check, save_just_highscore, load_all


def game_init():
    story.navigation_intro()
    out = [[deco.line_r()], ["Do you want to play this game as a rogue like?", ""], [1, "No", "Yes"], [deco.line_r()]]
    user.settings["delete_save_on_death"] = bool(u_KeyInput.keyinput(out))
    out = [[deco.line_r()], ["Should everything be centered?", "(you can change it later as well)", ""], [1, "No", "Yes"], [deco.line_r()]]
    user.settings["centered_screen"] = bool(u_KeyInput.keyinput(out))

    quests.init_quests()
    unlocks_init()
    location_init()
    u_KeyInput.name_init()
    story.intro_1()
    user.restart()
    u_KeyInput.display_shortcuts(True)


def partial_restart():
    user.restart()


def main():
    playing = True
    if not save_check():
        game_init()

    while playing:

        highscore = highscore_check()
        deco.clear_screen()
        overflow = ""
        while user.Player["hp"] > 0:

            overflow = show_location_actions.show_location_actions(get_location(), overflow)

            if user.Player["retired"]:
                break

        if user.Player["hp"] <= 0:
            user.Player["deaths"] += 1

        if user.settings["delete_save_on_death"]:
            save_just_highscore()

        else:
            save_update_score()

        if user.Player["hp"] > 0:
            out = story.outro_alive()
            n_print(out)
            time.sleep(1)
        else:
            out = story.outro_death()
            n_print(out)
            time.sleep(1)
        out += deco.line_r() + "\n"

        if user.Player["score"] > highscore:
            out += f'You have a new highscore of {colors.light_blue}{user.Player["score"]} Points{colors.reset}!\n'
        else:
            out += (f'You managed to get {colors.light_blue}{user.Player["score"]} Points{colors.reset}!\n'
                  f'Your highscore is {colors.light_blue}{highscore} Points{colors.reset}.\n')

        if user.Player["deaths"] > 1:
            out += f'You died {colors.red}{user.Player["deaths"]} times{colors.reset} to get this far.\n\n'

        if not user.settings["delete_save_on_death"]:
            out += ("I hope you've had fun with my small project. :)\n"
            "You can make a screenshot to save the score. ^^\n")
            out += deco.line_r() + "\n" + "What would you like to do?"
            options = [[out], [
                1,
                "Quit",
                "Complete restart",
                "Partial restart",
                "Load save"]]
            pick = u_KeyInput.keyinput(options)
            if not pick:
                break
            elif pick == 1:
                location_actions.restart()
            elif pick == 2:
                partial_restart()
            else:
                load_all()

        else:
            out += ("I hope you've had fun with my small project. :)\n"
                    "You can make a screenshot to save the score. ^^\n")
            out += deco.line_r() + "\n" + "What would you like to do?"
            options = [[out], [
                1,
                "Quit",
                "Restart"
            ]]
            pick = u_KeyInput.keyinput(options)
            if not pick:
                break
            else:
                game_init()

if __name__ == '__main__':
    terminal_funcs.init_keyboard_input()
    crafting.item_init()
    init_print.init_print()
    #u_KeyInput.keyboard_layout_init()
    u_KeyInput.options_open = False
    main()