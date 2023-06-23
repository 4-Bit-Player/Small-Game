# To do:
"""
    Mob drop
    Finding/unlocking stuff instead of fighting mobs
    Making everything moar beautiful
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    More locations
    more shops
    more things
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Working inventory system
    Crafting system
    Equipment
    Inven use

 """

import time
from decoration import story, deco, colors
from player import user
from places import show_location_actions, location_actions


def highscore_check():
    highscore_file = "highscore.txt"

    try:
        file_high = open(highscore_file, 'r')
        try:
            check_highscore = int(file_high.read())
        except ValueError:
            check_highscore = 0
        file_high.close()
        return check_highscore
    except IOError:
        open(highscore_file, 'w').close()
        check_highscore = 0
        return check_highscore


def restart():
    show_location_actions.init_places()
    location_actions.restart()
    user.restart()


playing = True

show_location_actions.init_places()




while playing:

    story.intro_1()
    highscore = highscore_check()

    deco.clear_l(s="", clear_all=1)

    while user.Player["hp"] > 0:

        deco.player_hud()

        show_location_actions.show_location_actions(location_actions.location)

        if user.Player["retired"]:
            break

    if user.Player["hp"] > 0:
        story.outro_alive()

    deco.clear_l(1)

    if user.Player["hp"] <= 0:
        story.outro_death()
        time.sleep(1)

    deco.clear_l()

    if user.Player["score"] > highscore:
        file = open("highscore.txt", 'w')
        file.write(str(user.Player["score"]))
        file.close()
        print(f'You have a new highscore of {colors.light_blue}{user.Player["score"]} Points{colors.reset}!')
    else:
        print(f'You managed to get {colors.light_blue}{user.Player["score"]} Points{colors.reset}!')

    print("I hope you've had fun with my small project. :)")
    str(input("You can make a screenshot to save the score. ^^"))
    print("Would you like to restart?")
    print("1. Yes")
    print("2. No")
    pick = user.user_input(2)
    if pick == 1:
        break
    else:
        restart()
