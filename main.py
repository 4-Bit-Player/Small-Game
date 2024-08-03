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
    Quests
    more recipies (and also switching to selection)
    Working inventory system
    Saves work + completely revamped
    Improved Crafting inventory
    upgrading of equipment
    possible to sell stuff
    moar Equipment
 """

import time
import pickle
from decoration import story, deco, colors
from player import user, crafting
from places import show_location_actions, location_actions, quest_logic, quests


def name_init():
    user.Player["name"] = user.Player_default["name"] = input("Please enter your name:")


def save_check():
    try:
        with open("save.pkl", "rb") as save_file:
            save = pickle.load(save_file)

        location_actions.highscore = save["highscore"]

        test = save["Player"]

        if not test:
            game_init()
            return

        if "Version" not in save:
            pass
        elif save["Version"] not in user.Compatible_versions:
            pass
        else:
            deco.clear_l()
            print("Save detected.\n"
                  "Would you like to load saved data?\n"
                  "1. Yes\n"
                  "2. No")
            deco.clear_l()

            user_pick = user.user_input(2)

            if not user_pick:
                if not location_actions.try_load_save(save):
                    game_init()
                return
            game_init()
            return
        print("Non Compatible save detected.\n"
              "Would you like to try and load the character?\n"
              "1. Yes\n"
              "2. No")
        user_pick = user.user_input(2)
        if not user_pick:
            if not location_actions.try_load_saved_player(save):
                game_init()
            return
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
    quests.init_quests()
    location_actions.unlocks_init()
    location_actions.location_init()
    name_init()
    story.intro_1()
    user.restart()


def save_update_score():
    try:
        with open("save.pkl", "rb") as save_file:
            save = pickle.load(save_file)
            save_file.close()

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


def restart():
    quests.init_quests()
    location_actions.unlocks_init()
    location_actions.location_init()
    location_actions.restart()
    user.restart()


playing = True
crafting.item_init()
save_check()

while playing:

    highscore = location_actions.highscore_check()
    deco.clear_l(1, "")

    while user.Player["hp"] > 0:

        show_location_actions.show_location_actions(location_actions.location)

        if user.Player["retired"]:
            break

    if user.Player["hp"] <= 0:
        user.deaths += 1

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
        print(f'You managed to get {colors.light_blue}{user.Player["score"]} Points{colors.reset}!\n'
              f'Your highscore is {colors.light_blue}{highscore} Points{colors.reset}.')

    if user.deaths > 1:
        print(f'You died {colors.red}{user.deaths} times{colors.reset} to get this far.\n')

    if not location_actions.settings["delete_save_on_death"]:
        print("I hope you've had fun with my small project. :)")
        str(input("You can make a screenshot to save the score. ^^"))
        print("What would you like to do?\n",
              "1. Quit\n",
              "2. Complete restart\n",
              "3. Partial restart",)
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
        print("What would you like to do?\n",
              "1. Quit\n",
              "2. Restart")
        pick = user.user_input(2)
        if not pick:
            break
        else:
            game_init()
