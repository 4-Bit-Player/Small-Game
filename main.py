# To do:
"""
    Making everything moar beautiful
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    More locations
    more shops
    more items
    more recipies (and also switching to selection)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Ask Surly about character
    Working inventory system
    moar Equipment
    Inventory use
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    At some point:
    changing input, so you can navigate using text
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Add NPCs
    quests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Added/Changed:
    Saves work
    Improved Crafting inventory
    upgrading of equipment
    possible to sell stuff
    moar Equipment
 """

import time
import dill
from decoration import story, deco, colors
from player import user
from places import show_location_actions, location_actions


def name_init():
    user.Player["name"] = user.Player_default["name"] = input("Please enter your name:")


def save_check():
    try:
        with open("save.pkl", "rb") as save_file:
            save = dill.load(save_file)
            save_file.close()
            location_actions.highscore = save["highscore"]

            test = save["Player"]

            if not test:
                game_init()
                return

            deco.clear_l()
            print("Save detected.")
            print("Would you like to load saved data?")
            print("1. Yes")
            print("2. No")
            deco.clear_l()

            user_pick = user.user_input(2)

            if not user_pick:
                try:
                    user.Player = save["Player"]
                    user.Equipped = save["Player_equip"]
                    location_actions.locations = save["locations"]
                    location_actions.location = save["location"]
                    location_actions.past_location = save["past_location"]
                    location_actions.settings = save["settings"]
                    show_location_actions.init_unlock()

                    deco.clear_l(1)
                    print(colors.green, "Save loaded successfully!", colors.reset)
                    deco.clear_l()
                    str(input("Press enter to continue your journey."))

                except KeyError:
                    deco.clear_l(1)
                    print(colors.red, "Unable to load save!", colors.reset)
                    deco.clear_l()
                    str(input("Press enter to start from the beginning."))
                    deco.clear_l(1, "")
                    game_init()

            else:
                game_init()

    except (FileNotFoundError, KeyError):
        game_init()


def game_init():
    deco.clear_l(1)
    print("Do you want to play this game as a rogue like?")
    print("1. No")
    print("2. Yes")
    deco.clear_l()
    location_actions.settings["delete_save_on_death"] = user.user_input(2)
    deco.clear_l(1, "")

    show_location_actions.init_unlock()
    show_location_actions.init_places()
    name_init()
    story.intro_1()


def save_update_score():
    try:
        with open("save.pkl", "rb") as save_file:
            save = dill.load(save_file)
            save_file.close()

            save["highscore"] = user.Player["score"] if user.Player["score"] > highscore else highscore
            updated_save = {key: value for key, value in save.items()}
            with open("save.pkl", "wb") as u_save_file:
                dill.dump(updated_save, u_save_file)
                u_save_file.close()

    except (FileNotFoundError, KeyError):
        save = {
            "highscore": user.Player["score"]
        }
        with open("save.pkl", "wb") as save_file:
            dill.dump(save, save_file)
            save_file.close()


def partial_restart():
    user.restart()


def restart():
    show_location_actions.init_unlock()
    show_location_actions.init_places()
    location_actions.restart()
    user.restart()


playing = True

save_check()

while playing:

    highscore = location_actions.highscore_check()
    deco.clear_l(1, "")

    while user.Player["hp"] > 0:
        deco.player_hud()

        show_location_actions.show_location_actions(location_actions.location)

        if user.Player["retired"]:
            break

    if location_actions.settings["delete_save_on_death"]:
        location_actions.save_just_highscore()

    else:
        save_update_score()

    if user.Player["hp"] > 0:
        story.outro_alive()
        time.sleep(1)
    else:
        story.outro_death()
        time.sleep(1)

    deco.clear_l()

    if user.Player["score"] > highscore:
        print(f'You have a new highscore of {colors.light_blue}{user.Player["score"]} Points{colors.reset}!')
    else:
        print(f'You managed to get {colors.light_blue}{user.Player["score"]} Points{colors.reset}!')

    if not location_actions.settings["delete_save_on_death"]:
        print("I hope you've had fun with my small project. :)")
        str(input("You can make a screenshot to save the score. ^^"))
        print("What would you like to do?")
        print("1. Quit")
        print("2. Complete restart")
        print("3. Partial restart")
        pick = user.user_input(3)
        if not pick:
            break
        elif pick == 2:
            partial_restart()
        else:
            restart()

    else:
        print("I hope you've had fun with my small project. :)")
        str(input("You can make a screenshot to save the score. ^^"))
        print("What would you like to do?")
        print("1. Quit")
        print("2. Restart")
        pick = user.user_input(2)
        if not pick:
            break
        else:
            game_init()
