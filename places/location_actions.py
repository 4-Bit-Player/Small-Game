#import json
import pickle
import random
import time
from places import unlock, quest_logic
from places import locations as loc
from copy import deepcopy
import combat
from decoration import deco, colors, story
from player import user, crafting, u_KeyInput

unlocks = {}
unlocked = {}
locations = []
location = {}
past_location = {}
weather_timer = 0
weather_day = "sunny"
settings = {
    "delete_save_on_death": 0,
}


def unlocks_init():
    global unlocks
    unlocks = unlock.unlocks


def load_saved_unlocks(things:list):
    r_unlocks = []
    for u_lock in things:
        r_unlocks.append(search_for_unlock(u_lock))
    return r_unlocks


def location_init():
    global locations
    global location
    global past_location
    locations = loc.locations = deepcopy(loc.default_locations)
    location = locations[0]
    past_location = location


def weather(current_location):
    global weather_timer
    global weather_day
    if current_location["type"] != "shop":
        if weather_timer == 0:
            weather_r = random.randint(1, 100)
            if weather_r <= int(current_location["weather"][0]):
                weather_day = "sunny"
            elif weather_r <= int(current_location["weather"][1]):
                weather_day = "cloudy"
            else:
                weather_day = "rainy"

            weather_timer += 4
        weather_timer -= 1
        current_location["true_weather"] = weather_day
    return current_location


def change_location():
    global location
    global past_location

    if len(location["list_of_actions"][0]["available_locations"]) == 1:
        pick = next(iter(location["list_of_actions"][0]["available_locations"].values()))
        if pick == "back":
            location_back()
        else:
            for i in locations:
                if i["name"] == pick:
                    past_location = location
                    location = i
                    deco.clear_screen()

    else:
        print("Where would you like to go?")
        option = 0
        current_list = []

        for index, k in list(location["list_of_actions"][0]["available_locations"].items()):
            option += 1
            print(f'{option}. {index}')
            current_list.append(k)
        pick = user.user_input(option)

        print(current_list[pick])
        if current_list[pick] == "back":
            location_back()
            deco.clear_screen()

        elif current_list[pick] != "stay":
            for i in locations:
                if i["name"] == current_list[pick]:
                    past_location = location
                    location = i
                    deco.clear_screen()
        else:
            deco.clear_screen()


def location_back():
    global location
    global past_location
    location, past_location = past_location, location
    deco.clear_screen()


def go_to_location(location_name):
    global location
    global past_location
    past_location = location
    location = search_location(location_name["name"])
    deco.clear_screen()


def shop(item):
    if check_money(item["price"]):
        crafting.item_add(item["item"])

        if isinstance(item["name"], list):
            pick = int(user.random_pick_list(item["name"]))

            item_name = item["name"][pick]

        else:
            item_name = item["name"]
        article = "an" if item_name.lower() in ["a", "e", "i", "o", "u"] else "a"
        deco.clear_screen()
        print(f'You bought {article} {item_name}')
    else:
        deco.clear_screen()
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


def check_hp_max():
    if user.Player["hp"] > user.Player["hp_max"]:
        user.Player["hp"] = user.Player["hp_max"]


def check_money(price):
    if user.Player["gold"] >= price:
        user.Player["gold"] -= price
        return True
    else:
        return False


def retire_check():
    deco.clear_screen()
    options = ["No", "Yes"]
    pick = u_KeyInput.keyinput(options, "Are you sure that you want to retire?")
    if pick == 1:
        user.Player["retired"] = True


def search_location(location_name: str):
    for i in locations:
        if i["name"] == location_name:
            return i


def restart():
    global location
    global past_location
    global weather_timer

    past_location = search_location("Forest")
    location = search_location("Castell City")
    weather_timer = 0


def inspect(current_location):
    curr_name = current_location["name"]
    if not current_location["inspect"]:
        deco.clear_l(1)
        print("You've seen everything here.")

    elif user.test:
        for thing in current_location["inspect"]:
            print(thing)
            if thing["unlocks"]:
                unlock_stuff(thing)
            if curr_name not in unlocked:
                unlocked[curr_name] = {}
                unlocked[curr_name]["inspect"] = [thing["u_name"]]
                continue
            unlocked[curr_name]["inspect"].append(thing["u_name"])
        current_location["inspect"].clear()
        deco.clear_screen()
        return

    else:
        options = [x["broad_desc"] for x in current_location["inspect"]]

        pick = u_KeyInput.keyinput(options, "Where do you want to go?")

        to_unlock = current_location["inspect"].pop(pick)
        story.show_text(to_unlock["text"])
        if to_unlock["unlocks"]:
            unlock_stuff(to_unlock)
        if curr_name not in unlocked:
            unlocked[curr_name] = {}
            unlocked[curr_name]["inspect"] = [to_unlock["u_name"]]
        else:
            unlocked[curr_name]["inspect"].append(to_unlock["u_name"])

    print("Press enter to continue.")
    u_KeyInput.wait_for_keypress()
    deco.clear_screen()
    return


def look_around(current_location):
    pick = random.randint(1, 1000)
    deco.clear_l(1)
    print(f'You are wandering through the {current_location["name"]} looking for usable Items...')
    time.sleep(random.uniform(0.5, 2))
    if pick <= current_location["enemy_chance"]:
        print("Suddenly you hear something behind you.")
        time.sleep(1)
        combat.combat(current_location)

    elif pick <= current_location["item_find_chance"]:
        drop_malus = 0
        findable_items = list(current_location["findable_items"].keys())
        random.shuffle(findable_items)

        for item in findable_items:
            it_pick = random.randint(1, 1000)

            item_ending = ""

            drop_chances = current_location["findable_items"][item]
            for amount, chance in drop_chances.items():
                if it_pick <= chance - drop_malus:
                    crafting.item_add(item, amount)
                    drop_malus += 100
                    if amount >= 2:
                        item_ending = "s"

                    time.sleep(1.3)
                    print(f'You found {colors.green}{amount}x {item}{item_ending}{colors.reset}.')

                    break

        time.sleep(1)
        if drop_malus == 0:
            print("You didn't find anything useful...")

        print("Press enter to continue...")
        u_KeyInput.wait_for_keypress()
        deco.clear_screen()


def unlock_stuff(stuff_to_unlock):
    # print("Stuff: ", stuff_to_unlock)
    if isinstance(stuff_to_unlock, list):
        for thing in stuff_to_unlock:
            place = search_location(thing["unlock_location"])
            real_unlock = search_for_unlock(thing["unlocks"])
            if real_unlock["type"] == "actions":
                place["list_of_actions"].append(real_unlock)
        return
    if not stuff_to_unlock["unlocks"]:
        return

    place = search_location(stuff_to_unlock["unlock_location"])
    real_unlock = search_for_unlock(stuff_to_unlock["unlocks"])
    if real_unlock is None:
        return
    if real_unlock["type"] == "actions":
        place["list_of_actions"].append(real_unlock)


def search_for_unlock(name):
    return unlocks[name]


def load_unlocked(stuff_to_unlock: dict):
    for place, sec_dict in stuff_to_unlock.items():
        t_location = search_location(place)
        for unlock_type, u_locks in sec_dict.items():
            for u_lock_name in u_locks:
                print(u_lock_name, "\n", unlock_type)
                if u_lock_name not in unlocks:
                    continue
                u_lock = search_for_unlock(u_lock_name)
                print(u_lock)
                print(t_location)
                t_location[unlock_type].remove(u_lock)
                unlock_stuff(u_lock)


def save_load():
    options = [
        "Go back.",
        "Save the game",
        "Load saved game"
    ]
    pick = u_KeyInput.keyinput(options, "What do you want to do?", )
    if not pick:
        return
    if pick == 1:
        save_all()
    else:
        load_all()


def save_all():
    options = [
        ["Are you sure?",
         "Already saved data will be overwritten."],
        "No",
        "Yes",

    ]

    pick = u_KeyInput.keyinput(options, "Saving Game")
    if not pick:
        return

    else:
        highscore = highscore_check()
        finished_quests, active_quests = quest_logic.generate_quests_for_save()
        save = {
            "Player": user.Player,
            "Player_equip": user.Equipped,
            "highscore": highscore,
            "settings": settings,
            "Version": user.Version,
            "unlocked": unlocked,
            "location": location["name"],
            "past_location": past_location["name"],
            "finished_quests": finished_quests,
            "active_quests": active_quests,
            "deaths": user.deaths

        }
        with open("save.pkl", "wb") as save_file:
            pickle.dump(save, save_file)
            save_file.close()
        user.character_loaded = True

        deco.clear_l(1)
        print(colors.green, "Game saved successfully!", colors.reset)
        deco.clear_l()
        print("Press enter to continue.")
        u_KeyInput.wait_for_keypress()
        deco.clear_screen()


def load_all():
    options = [
        ["Are you sure?",
         "Your current progress will be overwritten."],
        "No",
        "Yes",

    ]
    pick = u_KeyInput.keyinput(options, "Loading Game")
    if not pick:
        return

    try:
        with open("save.pkl", "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(colors.red, "No file found!", colors.reset)
        print("Press enter to continue.")
        u_KeyInput.wait_for_keypress()
        return
    if "Version" not in data:
        pass
    elif data["Version"] not in user.Compatible_versions:
        pass
    else:
        try_load_save(data)
        return
    out = ("Version not compatible. Should only the Character get loaded?\n"
           "1. Yes\n"
           "2. No")
    print(out)
    pick = user.user_input(2)
    if pick:
        return
    try_load_saved_player(data)


def highscore_check():
    try:
        with open("save.pkl", "rb") as save_file:
            saved_data = pickle.load(save_file)
            save_file.close()
            score = saved_data["highscore"]

    except (FileNotFoundError, KeyError):
        score = 0

    return score


def save_just_highscore():
    try:
        with open("save.pkl", "rb") as save_file:
            saved_data = pickle.load(save_file)
            save_file.close()
            saved_score = saved_data["highscore"]
    except (FileNotFoundError, KeyError):
        saved_score = 0

    score = user.Player["score"] if user.Player["score"] >= saved_score else saved_score
    save_data = {"highscore": score}
    
    with open("save.pkl", "wb") as save_file:
        pickle.dump(save_data, save_file)
        save_file.close()


def try_load_save(save, active_game=False):
    global location
    global past_location
    global settings
    global unlocked
    unlocks_init()
    location_init()
    lookup = ["Player", "Player_equip", "location", "past_location", "settings",
              "unlocked", "finished_quests", "active_quests", "deaths"]
    broken = False
    for thing in lookup:
        if thing not in save:
            broken = True
            break

    if not broken:
        user.Player = save["Player"]
        user.Equipped = save["Player_equip"]
        user.deaths = save["deaths"]
        user.character_loaded = True
        location = search_location(save["location"])
        past_location = search_location(save["past_location"])
        settings = save["settings"]
        unlocked = save["unlocked"]
        finished_q = save["finished_quests"]
        active_q = save["active_quests"]
        quest_logic.load_saved_quests(finished_q, active_q)

        load_unlocked(unlocked)
        deco.full_clear() # required, because of the tons of text
        deco.clear_l()
        print(colors.green, "Save loaded successfully!", colors.reset)
        deco.clear_l()
        print("Press enter to continue your journey.")
        u_KeyInput.wait_for_keypress()
        deco.clear_screen()
        return True

    else:
        deco.clear_l(1)
        print(colors.red, "Unable to load save!", colors.reset)
        deco.clear_l()
        if not active_game:
            print("Press enter to start from the beginning.")
        else:
            print("Press enter to continue.")
        u_KeyInput.wait_for_keypress()
        deco.clear_screen()
        return False


def try_load_saved_player(save, active_game=False):
    global settings
    unlocks_init()
    location_init()
    broken = False
    lookup = ["Player", "Player_equip", "settings"]
    for thing in lookup:
        if thing not in save:
            broken = True
            break
    if not broken:
        user.Player = save["Player"]
        user.Equipped = save["Player_equip"]
        settings = save["settings"]
        if "deaths" in save:
            user.deaths = save["deaths"]
        else:
            user.deaths = 0
        user.character_loaded = True
        deco.full_clear() # Most likely isn't required
        deco.clear_l()
        print(colors.green, "Player data loaded successfully!", colors.reset)
        deco.clear_l()
        print("Press enter to continue your journey.")
        u_KeyInput.wait_for_keypress()
        return True

    else:
        deco.clear_l(1)
        print(colors.red, "Unable to load player data!", colors.reset)
        deco.clear_l()
        if not active_game:
            print("Press enter to start from the beginning.")
        else:
            print("Press enter to continue.")
        u_KeyInput.wait_for_keypress()
        deco.clear_screen()
        return False
