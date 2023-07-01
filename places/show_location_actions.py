import player.inventory
from decoration import *
from places import location_actions, locations, unlock
from player import *
import enemies
import combat
import copy


def show_location_actions(current_location):
    deco.print_header(current_location["name"])
    for i in current_location["welcome_text"]:
        deco.print_in_line(i)

    if current_location["type"] not in ["shop", "Blacksmith"]:
        current_location = location_actions.weather(current_location)
        print(f'It is a {current_location["true_weather"]} day.')
        deco.clear_l()

    else:
        print()
        print("What do you want to do?")
        deco.clear_l()

    user.show_pick_actions_dict(current_location["list_of_actions"])

    try:
        if current_location["type"] == "City":
            num = len(current_location["list_of_actions"]) + 1
            print(f"{num}. Open Inventory")
            print(f"{num+1}. Retire here")
            print(f"{num+2}. Save/Load")
            pick = int(user.user_input(num+2))

        elif current_location["type"] in ["Wilderness", "shop"]:
            num = len(current_location["list_of_actions"]) + 1
            print(f"{num}. Open Inventory")
            pick = int(user.user_input(num))

        else:
            pick = int(user.user_input(len(current_location["list_of_actions"])))

    except TypeError:
        pick = int(user.user_input(len(current_location["list_of_actions"])))

    if pick <= len(current_location["list_of_actions"]) - 1:

        pot_function = current_location["list_of_actions"][pick]["action_type"]

        if isinstance(pot_function, str):

            function = globals()[pot_function]
            if pot_function == "re_encounter":
                function(current_location)
            elif pot_function == "inspect":
                function(current_location)
            elif pot_function == "shop":
                function(current_location["list_of_actions"][pick])
            else:
                function()

        if pot_function in [enemies.encounter, location_actions.inspect, combat.combat, location_actions.look_around]:
            pot_function(current_location)
        elif pot_function in [location_actions.shop, location_actions.go_to_location]:
            pot_function(current_location["list_of_actions"][pick])
        else:
            pot_function()

    else:
        if pick == len(current_location["list_of_actions"]):
            player.inventory.open_inventory()

        elif pick == len(current_location["list_of_actions"]) + 1:
            location_actions.retire_check()

        else:
            location_actions.save_load()


def init_places():
    location_actions.location_init(copy.deepcopy(locations.locations))


def init_unlock():
    location_actions.unlocks_init(copy.deepcopy(unlock.unlocks))


def settings_init():

    settings = location_actions.settings = {
        "delete_save_on_death": 0,
    }
