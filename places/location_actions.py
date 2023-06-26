import random
import time

import combat
from decoration import *
from player import user, crafting


locations = []
location = locations
weather_timer = 0
weather_day = "sunny"


def location_init(list_of_locations):
    global locations
    global location
    locations = list_of_locations
    location = locations[0]


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
                    deco.clear_l(clear_all=1)

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

        elif current_list[pick] != "stay":
            for i in locations:
                if i["name"] == current_list[pick]:
                    past_location = location
                    location = i
                    deco.clear_l(clear_all=1)


def location_back():
    global location
    global past_location
    temp = location
    location = past_location
    past_location = temp

    deco.clear_l(clear_all=1)


def go_to_location(location_name):
    global location
    global past_location
    past_location = location
    location = search_location(location_name["name"])
    deco.clear_l(s="", clear_all=1)


def shop(item):

    if check_money(item["price"]):

        r_item = crafting.item_search(item["item"])
        crafting.item_add(r_item)

        if isinstance(item["name"], list):
            pick = int(user.random_pick_list(item["name"]))

            item_name = item["name"][pick]

        else:
            item_name = item["name"]
        article = "an" if item_name.lower() in ["a", "e", "i", "o", "u"] else "a"
        deco.clear_l(s="", clear_all=1)
        print(f'You bought {article} {item_name}')
    else:
        deco.clear_l(s="", clear_all=1)
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
    print("Are you sure that you want to retire?")
    print("1. Yes")
    print("2. No")
    pick = user.user_input(2)
    if pick == 0:
        user.Player["retired"] = True


def search_location(location_name):
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
    story.show_text(current_location["inspect"])
    combat.combat(current_location)


past_location = search_location("Forest")


def look_around(current_location):
    pick = random.randint(1, 1000)
    if pick <= current_location["enemy_chance"]:
        deco.clear_l(1)
        print(f'You are wandering through the {current_location["name"]} looking for usable Items...')
        time.sleep(1)
        print("Suddenly you hear something behind you.")
        time.sleep(1)
        combat.combat(current_location)

    elif pick <= current_location["item_find_chance"]:

        deco.clear_l(1)

        print(f'You are wandering through the {current_location["name"]} looking for usable Items...')
        drop_malus = 0
        findable_items = list(current_location["findable_items"].keys())
        random.shuffle(findable_items)

        for item in findable_items:
            it_pick = random.randint(1, 1000)

            item_ending = ""

            drop_chances = current_location["findable_items"][item]
            for amount, chance in drop_chances.items():
                if it_pick <= chance - drop_malus:
                    real_item = crafting.item_search(item)
                    crafting.item_add(real_item, amount)
                    drop_malus += 100
                    if amount >= 2:
                        item_ending = "s"

                    time.sleep(1.3)
                    print(f'You found {colors.green}{amount}x {item}{item_ending}{colors.reset}.')

                    break

        time.sleep(1)
        if drop_malus == 0:
            print("You didn't find anything useful...")

        str(input("Press enter to continue"))
        deco.clear_l(s="", clear_all=1)
