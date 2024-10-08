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
import pickle
from decoration import story, deco, colors
from player import user, crafting, u_KeyInput
from places import show_location_actions, location_actions, quests
from printing import init_print
from printing.print_queue import n_print


def save_check():
    try:
        with open("save.pkl", "rb") as save_file:
            save = pickle.load(save_file)


        if not "Player" in save:
            game_init()
            return

        if "Version" not in save:
            pass
        elif save["Version"] not in user.Compatible_versions:
            pass
        else:
            options = [
                [deco.line_r(),
                 "Save detected.",
                 "Would you like to load the save data?",],
                "Yes",
                "No",
                [deco.line_r()]
                 ]
            user_pick = u_KeyInput.keyinput(options)

            if not user_pick:
                if not location_actions.try_load_save(save):
                    game_init()
                return
            game_init()
            return
        options = [["Non Compatible save detected.",
              "Would you like to try and load the character?\n"],
              "Yes",
              "No"]
        user_pick = u_KeyInput.keyinput(options)
        if not user_pick:
            if not location_actions.try_load_saved_player(save):
                game_init()
            return
        game_init()

    except (FileNotFoundError, KeyError):
        game_init()


def game_init():
    out = [[deco.line_r()], ["Do you want to play this game as a rogue like?", ""], [1, "No", "Yes"], [deco.line_r()]]
    user.settings["delete_save_on_death"] = bool(u_KeyInput.keyinput(out))
    out = [[deco.line_r()], ["Should everything be centered?", "(you can change it later as well)", ""], [1, "No", "Yes"], [deco.line_r()]]
    user.settings["centered_screen"] = bool(u_KeyInput.keyinput(out))

    quests.init_quests()
    location_actions.unlocks_init()
    location_actions.location_init()
    u_KeyInput.name_init()
    story.intro_1()
    user.restart()


def save_update_score():
    try:
        with open("save.pkl", "rb") as save_file:
            save = pickle.load(save_file)
            save_file.close()
        highscore = 0
        if "highscore" in save:
            highscore += save["highscore"]

        save["highscore"] = user.Player["score"] if user.Player["score"] > highscore else highscore
        if user.character_loaded:
            save["deaths"] = user.deaths

        with open("save.pkl", "wb") as u_save_file:
            pickle.dump(save, u_save_file)
            u_save_file.close()

    except (FileNotFoundError, KeyError):
        save = {
            "highscore": user.Player["score"]
        }
        with open("save.pkl", "wb") as save_file:
            pickle.dump(save, save_file)
            save_file.close()


def partial_restart():
    user.restart()


def main():
    playing = True
    save_check()
    while playing:

        highscore = location_actions.highscore_check()
        deco.clear_screen()
        overflow = ""
        while user.Player["hp"] > 0:

            overflow = show_location_actions.show_location_actions(location_actions.location, overflow)

            if user.Player["retired"]:
                break

        if user.Player["hp"] <= 0:
            user.Player["deaths"] += 1

        if user.settings["delete_save_on_death"]:
            location_actions.save_just_highscore()

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
                location_actions.load_all()

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
    crafting.item_init()
    init_print.init_print()
    u_KeyInput.keyboard_layout_init()
    u_KeyInput.options_open = False
    main()