from player.keyinput_index_class import KeyinputIndexClass
from save_system.save_logic import save_load
from player import u_FullKeyInput
from decoration import *
from places import location_actions, shop, quest_logic, location_data, look_around_funcs
from player import *
import enemies
import combat
from printing.print_queue import n_print

def show_location_actions(current_location, overflow):
    options = [[deco.format_text_in_line(current_location["welcome_text"])]]

    if current_location["type"] not in ["shop", "forge"]:
        current_location = location_data.weather(current_location)
        options.append(
            [
                f'It is a {current_location["true_weather"]} day.',
                deco.line_r()
            ]
        )

    else:
        options.append([
            "\nWhat do you want to do?",
            deco.line_r()
        ])

    options += user.return_pick_actions_dict(current_location["list_of_actions"])

    if current_location["type"] in ["Wilderness"]:
        pass

    elif current_location["type"] == "City":
        options += [
            f"Retire here",
            f"Save/Load"
        ]

    elif current_location["type"] in ["shop"]:
        pass

    if overflow:
        options.append([overflow])
        overflow = ""
    if "index_class" in current_location:
        if current_location["index_class"] is not None:
            options.insert(0, current_location["index_class"])
    pick = u_FullKeyInput.keyinputfull(options, header=current_location["name"], hud=True)
    if isinstance(options[0], KeyinputIndexClass):
        current_location["index_class"] = options[0]

    if pick <= len(current_location["list_of_actions"]) - 1:

        pot_function = current_location["list_of_actions"][pick]["action_type"]

        if isinstance(pot_function, str):
            if pot_function in ["encounter", "inspect", "combat", "look_around"]:
                actions[pot_function](current_location)
            elif pot_function in ["shop", "go_to_location", "buy"]:
                overflow = actions[pot_function](current_location["list_of_actions"][pick])
            else:
                actions[pot_function]()

        else:
            n_print("Something is wrong with the actions: ", pot_function)

    else:
        if pick == len(current_location["list_of_actions"]):
            location_actions.retire_check()

        else:
            save_load()
    return overflow


actions = {"encounter": enemies.encounter,
           "inspect": location_actions.inspect,
           "combat": combat.combat,
           "look_around": look_around_funcs.look_around,
           "shop": location_actions.shop,
           "go_to_location": location_data.go_to_location,
           "buy": shop.buy,
           "shop_sell": shop.shop_sell,
           "re_encounter": 0,
           "change_location": location_actions.change_location,
           "open_inventory": inventory.open_inventory,
           "upgrading": crafting.upgrading,
           "check_active_quests": quest_logic.check_active_quests
           }
