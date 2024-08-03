from decoration import *
from places import location_actions, locations, unlock, shop, quest_logic
from player import *
import enemies
import combat


def show_location_actions(current_location):
    deco.print_header(current_location["name"])
    for i in current_location["welcome_text"]:
        deco.print_in_line(i)

    if current_location["type"] not in ["shop", "forge"]:
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
            print(f"{num}. Retire here")
            print(f"{num+1}. Save/Load")
            pick = int(user.user_input(num+1))

        elif current_location["type"] in ["Wilderness", "shop"]:
            num = len(current_location["list_of_actions"])
            pick = int(user.user_input(num))

        else:
            pick = int(user.user_input(len(current_location["list_of_actions"])))

    except TypeError:
        pick = int(user.user_input(len(current_location["list_of_actions"])))

    if pick <= len(current_location["list_of_actions"]) - 1:

        pot_function = current_location["list_of_actions"][pick]["action_type"]

        if isinstance(pot_function, str):
            if pot_function in ["encounter", "inspect", "combat", "look_around"]:
                actions[pot_function](current_location)
            elif pot_function in ["shop", "go_to_location", "buy"]:
                actions[pot_function](current_location["list_of_actions"][pick])
            else:
                actions[pot_function]()

        else:
            print("Something is wrong with the actions: ", pot_function)

    else:
        if pick == len(current_location["list_of_actions"]):
            location_actions.retire_check()

        else:
            location_actions.save_load()


actions = {"encounter": enemies.encounter,
           "inspect": location_actions.inspect,
           "combat": combat.combat,
           "look_around": location_actions.look_around,
           "shop": location_actions.shop,
           "go_to_location": location_actions.go_to_location,
           "buy": shop.buy,
           "shop_sell": shop.shop_sell,
           "re_encounter": 0,
           "change_location": location_actions.change_location,
           "open_inventory": inventory.open_inventory,
           "upgrading": crafting.upgrading,
           "check_active_quests": quest_logic.check_active_quests
           }
