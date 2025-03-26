#import json
import time
from decoration import colors, deco
from places import quest_logic, location_data, location_actions
from places.location_data import search_for_unlock, get_unlocked, get_location, get_past_location, unlocks_init, \
    location_init
from places.locations import search_location
from player import user, u_KeyInput
from player.u_KeyInput import keyinput, wait_for_keypress
from printing.print_queue import n_print
from save_system.file_system import save_game, get_save_nums, load_save, delete_save


def load_saved_unlocks(things:list):
    r_unlocks = []
    for u_lock in things:
        r_unlocks.append(search_for_unlock(u_lock))
    return r_unlocks



def load_unlocked(stuff_to_unlock: dict):
    for place, sec_dict in stuff_to_unlock.items():
        t_location = search_location(place)
        for unlock_type, u_locks in sec_dict.items():
            for u_lock_name in u_locks:
                print(u_lock_name, "\n", unlock_type)
                u_lock = search_for_unlock(u_lock_name)
                if u_lock is None:
                    print(colors.red + "Failed to find " + u_lock_name + colors.reset)
                    time.sleep(0.2)
                    #wait_for_keypress()
                    continue
                print(u_lock)
                print(t_location)
                t_location[unlock_type].remove(u_lock)
                location_actions.unlock_stuff(u_lock)


def _save_overwrite_confirmation() -> bool:
    options = [
        ["Are you sure?",
         "Already saved data will be overwritten."],
        "No",
        "Yes",
    ]
    return keyinput(options, "Saving Game") == 1

def save_all():

    highscore = highscore_check()
    finished_quests, active_quests = quest_logic.generate_quests_for_save()
    save = {
        "Player": user.Player,
        "Player_equip": user.Equipped,
        "highscore": highscore,
        "settings": user.settings,
        "Version": user.Version,
        "unlocked": get_unlocked(),
        "location": get_location()["name"],
        "past_location": get_past_location()["name"],
        "finished_quests": finished_quests,
        "active_quests": active_quests,
        "game_code": user.game_code,
    }

    if user.character_loaded and user.settings["delete_save_on_death"]:
        if not _save_overwrite_confirmation():
            return
        save_game(user.save_slot, save)
    else:
        nums = get_save_nums()
        saves = [f"Save file {x}" for x in range(10)]
        if user.character_loaded:
            if user.save_slot in nums:
                nums.pop(user.save_slot)
                saves[user.save_slot] += " (current save)"
        for i in nums:
            saves[i] += " (exists)"
        options = [
            [
                deco.line_r(),
                "Which save file do you want to use?",
                deco.line_r()
            ],
            "Back"
        ]
        options += saves

        pick = keyinput(options)
        if pick == 0:
            return
        if pick - 1 in nums:
            if not _save_overwrite_confirmation():
                return

        save_game(pick - 1, save)
        user.save_slot = pick - 1

    #with open("save.json", "w") as file:
    #   json.dump(save, file, indent=4)

    user.character_loaded = True
    n_print(
        deco.line_r() + "\n" +
        colors.green + "Game saved successfully!" + colors.reset + "\n" +
        deco.line_r() + "\n" +
        "Press enter to continue.\n"
    )
    wait_for_keypress()


def load_all():
    nums = get_save_nums()
    if len(nums) == 0:
        n_print(colors.red + "No Save File Found!" + colors.reset + "\n" + "Press enter to continue.\n")
        wait_for_keypress()
        return


    save_nums = ["Save " + str(x) for x in nums]

    options = [
        [deco.line_r(),
         "Which save do you want to load?\n(Your current progress will be overwritten.)", deco.line_r()],
        "Back",
        [""]
    ]
    options += save_nums

    pick = keyinput(options)
    if pick == 0:
        return

    data = load_save(nums[pick-1])

    if "Version" in data and data["Version"] in user.Compatible_versions:
        try_load_save(data, nums[pick-1])
        return
    if "player" in data:
        out = [["Version not compatible. Should only the Character get loaded?"],
               "Yes",
               "No"]
        pick = keyinput(out)
        if pick:
            return
        try_load_saved_player(data, nums[pick-1])
        return
    n_print("The save seems to be corrupted. D:\nPress enter to continue...")
    wait_for_keypress()


def highscore_check():
    save = load_save(-1)
    highscore = 0
    if "highscore" in save:
        highscore = save["highscore"]

    return highscore


def save_just_highscore():
    saved_score = 0
    saved_data = load_save(-1)
    if "highscore" in saved_data:
        saved_score = saved_data["highscore"]

    score = user.Player["score"] if user.Player["score"] >= saved_score else saved_score
    save_data = {"highscore": score}

    save_game(-1, save_data)
    if user.character_loaded and user.save_slot != -1:
        delete_save(user.save_slot)
        user.character_loaded = False


def try_load_save(save, save_num, active_game=False):
    lookup = ["Player", "Player_equip", "location", "past_location", "settings",
              "unlocked", "finished_quests", "active_quests", "Version", "game_code"]
    broken = False
    for thing in lookup:
        if thing not in save:
            broken = True
            break

    if not broken:
        if not save["Version"] in user.Compatible_versions:
            broken = True

    if not broken:
        user.restart()
        unlocks_init()
        location_init()
        user.Player.update(save["Player"])
        user.Equipped.update(save["Player_equip"])
        if "deaths" in save:
            if save["deaths"] > user.Player["deaths"]:
                user.Player["deaths"] = save["deaths"]
        user.character_loaded = True
        user.save_slot = save_num
        user.game_code = save["game_code"]
        location_data._location = search_location(save["location"])
        location_data._past_location = search_location(save["past_location"])
        user.settings.update(save["settings"])
        location_data._unlocked = save["unlocked"]
        finished_q = save["finished_quests"]
        active_q = save["active_quests"]
        quest_logic.load_saved_quests(finished_q, active_q)

        load_unlocked(save["unlocked"])
        deco.full_clear() # required, because of the tons of text
        out = (
            deco.line_r() + "\n" +
            f"{colors.green}Save loaded successfully!{colors.reset}\n" +
            deco.line_r() + "\nPress enter to continue your journey."
        )
        n_print(out)
        wait_for_keypress()
        return True


    out = (
        deco.line_r() + "\n" +
        f"{colors.red}Unable to load save!{colors.reset}\n" +
        deco.line_r() + "\n"
    )
    if not active_game:
        out += "Press enter to start from the beginning.\n"
    else:
        out += "Press enter to continue.\n"
    n_print(out)
    wait_for_keypress()
    return False


def try_load_saved_player(save, save_num):
    unlocks_init()
    location_init()
    user.restart()
    broken = False
    lookup = ["Player", "Player_equip", "settings", "game_code"]
    for thing in lookup:
        if thing not in save:
            broken = True
            break
    if not broken:
        user.Player.update(save["Player"])
        user.Equipped.update(save["Player_equip"])
        user.settings.update(save["settings"])
        user.game_code = save["game_code"]
        user.character_loaded = True
        user.save_slot = save_num
        deco.full_clear() # Most likely isn't required
        out = (
                deco.line_r() + "\n" +
                f"{colors.green}Player data loaded successfully!{colors.reset}\n" +
                deco.line_r() + "\nPress enter to continue your journey."
        )
        n_print(out)
        wait_for_keypress()
        return True

    else:
        out = (
                deco.line_r() + "\n" +
                f"{colors.red}Unable to load player data!{colors.reset}\n" +
                deco.line_r() + "\n" +
                "Press enter to start from the beginning.\n"
        )
        n_print(out)
        wait_for_keypress()
        return False


def save_load():
    options = [
        "Go back.",
        "Save the game",
        "Load saved game"
    ]
    pick = keyinput(options, "What do you want to do?", )
    if not pick:
        return
    if pick == 1:
        save_all()
    else:
        load_all()


def save_check() -> bool:
    save_nums = get_save_nums()
    if len(save_nums) == 0:
        return False
    options = [
        [deco.line_r(),
         "Save(s) detected.",
         "Would you like to load the saved data?",
         ],
        "Yes",
        "No",
        [deco.line_r()]
    ]
    pick = u_KeyInput.keyinput(options)
    if pick:
        return False

    options = [
        [deco.line_r(),
         "Which save do you want to load?", ""
         ],
        "Back",
        [""],
    ]
    options += [f"Save {x}" for x in save_nums]
    pick = u_KeyInput.keyinput(options)
    if not pick:
        return False
    picked_save = pick-1
    save = load_save(save_nums[picked_save])

    if not "Player" in save:
        n_print(colors.red + "The save seems to be broken. D:" + colors.reset+"\nPress enter to start from the beginning...")
        u_KeyInput.wait_for_keypress()
        return False

    if "Version" in save and save["Version"] in user.Compatible_versions:
        if try_load_save(save, picked_save):
            return True
        return False

    options = [["The version seems not compatible.",
          "Would you like to try and load the character?\n"],
          "Yes",
          "No"]
    user_pick = u_KeyInput.keyinput(options)
    if not user_pick:
        if try_load_saved_player(save, picked_save):
            return True
    return False


def save_update_score():
    save = load_save(-1)
    if save == "":
        save_game(-1,{"highscore": user.Player["score"]})
        return

    highscore = 0
    if "highscore" in save:
        highscore = save["highscore"]

    save["highscore"] = user.Player["score"] if user.Player["score"] > highscore else highscore

    for num in get_save_nums():
        if num == user.save_slot:
            continue
        n_save = load_save(num)
        if not "game_code" in n_save:
            continue
        if n_save["game_code"] != user.game_code:
            continue
        if not "Player" in n_save:
            continue
        n_save["Player"]["deaths"] = user.Player["deaths"]
        save_game(num, n_save)


    if user.character_loaded:
        user_save = load_save(user.save_slot)
        if "Player" in save:
            user_save["Player"]["deaths"] = user.Player["deaths"]
            save_game(user.save_slot, user_save)

    save_game(-1, save)
    return
