import random
import time
from places import quests
import combat
from decoration import deco, colors, story
from places.location_data import unlocks_init, location_init, \
    location_back, go_to_location, get_unlocked, get_location, search_for_unlock
from places.locations import search_location
from player import user, crafting
from printing.print_queue import n_print
from player.u_KeyInput import keyinput, wait_for_keypress, display_shortcuts


def change_location():
    location = get_location()
    if len(location["list_of_actions"][0]["available_locations"]) == 1:
        pick = next(iter(location["list_of_actions"][0]["available_locations"].values()))
        if pick == "back":
            location_back()
        else:
            go_to_location(pick)

    else:
        out = [["Where would you like to go?"]]
        option = 0
        current_list = []

        for index, k in list(location["list_of_actions"][0]["available_locations"].items()):
            option += 1
            out.append(f'{option}. {index}')
            current_list.append(k)
        n_print(out)
        pick = keyinput(option, hud=True)

        #print(current_list[pick])
        if current_list[pick] == "back":
            location_back()

        elif current_list[pick] != "stay":
            go_to_location(current_list[pick])



def shop(item):
    if check_money(item["price"]):
        crafting.item_add(item["item"])

        if isinstance(item["name"], list):
             item_name= random.choice(item["name"])

        else:
            item_name = item["name"]
        article = "an" if item_name.lower() in ["a", "e", "i", "o", "u"] else "a"
        return deco.line_r() + "\n" + f'You bought {article} {item_name}\n' + deco.line_r() + "\n"


    if isinstance(item["name"], list):
        item_name = item["name"][0]

    else:
        item_name = item["name"]
    article = "an" if item_name.lower() in ["a", "e", "i", "o", "u"] else "a"

    return (deco.line_r() + "\n" +
            f'{colors.red}You don\'t have enough money to buy {article} {item_name} right now.{colors.reset}' +
            deco.line_r() + "\n"
            )

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
    options = ["No", "Yes"]
    pick = keyinput(options, "Are you sure that you want to retire?")
    if pick == 1:
        user.Player["retired"] = True


def inspect(current_location):
    curr_name = current_location["name"]
    unlocked = get_unlocked()
    out = ""
    if not current_location["inspect"]:
        out += (deco.line_r() + "\nYou've seen everything here.\n")

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

        pick = keyinput(options, "Where do you want to go?")

        to_unlock = current_location["inspect"].pop(pick)
        out += story.show_text(to_unlock["text"])
        if to_unlock["unlocks"]:
            unlock_stuff(to_unlock)
        if curr_name not in unlocked:
            unlocked[curr_name] = {}
            unlocked[curr_name]["inspect"] = [to_unlock["u_name"]]
        else:
            unlocked[curr_name]["inspect"].append(to_unlock["u_name"])

    out += "Press enter to continue.\n"
    n_print(out)
    wait_for_keypress()
    deco.clear_screen()
    return


def look_around(current_location):
    pick = random.randint(1, 1000)
    out = deco.line_r() + f'\nYou are wandering through the {current_location["name"]} looking for usable Items...\n'
    n_print(out)
    time.sleep(random.uniform(0.5, 1.2))
    if pick <= current_location["enemy_chance"]:
        out += "Suddenly you hear something behind you.\n"
        n_print(out)
        time.sleep(1)
        combat.combat(current_location)
        return

    if pick <= current_location["item_find_chance"]:
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

                    out += f'You found {colors.green}{amount}x {item}{item_ending}{colors.reset}.\n'
                    n_print(out)
                    time.sleep(1.3)

                    break

        if drop_malus == 0:
            out += "You didn't find anything useful...\n"

        out += "Press enter to continue...\n"
        n_print(out)
        wait_for_keypress()


def restart():
    display_shortcuts(True)
    quests.init_quests()
    unlocks_init()
    location_init()
    user.restart()


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

