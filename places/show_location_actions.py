from decoration import *
from places import location_actions, locations
from player import *
import enemies
import combat
import copy


def show_location_actions(current_location):
    deco.print_header(current_location["name"])
    for i in current_location["welcome_text"]:
        deco.print_in_line(i)

    if current_location["type"] != "shop":
        current_location = location_actions.weather(current_location)
        print(f'It is a {current_location["true_weather"]} day.')
        deco.clear_l()

    else:
        print()
        print(f'You currently have{colors.gold} {round(user.Player["gold"], 1)} Gold{colors.reset}.')
        print("What do you want to do?")
        deco.clear_l()

    pick = user.show_pick_actions_dict(current_location["list_of_actions"])
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


def init_places():
    location_actions.location_init(copy.deepcopy(locations.locations))
