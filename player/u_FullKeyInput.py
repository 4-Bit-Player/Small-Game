import places.quest_logic
import player.inventory
from input_system import get_key, SpecialChar
from player import u_KeyInput
from decoration import colors, deco
from player.keyinput_index_class import KeyinputIndexClass, TempInput
from player.u_KeyInput import handle_number_keys, handle_backspace, handle_arrow_key, handle_f_keys
from printing import n_print


def keyinputfull(options: list, header: str = "", start_at=1, hud: bool = False):
    options = u_KeyInput.create_index(options)
    index_class:KeyinputIndexClass = options[0]
    temp_input: TempInput = index_class.temp_input

    invalid = False

    while True:
        out = ""
        if hud:
            out += deco.player_hud() + "\n"
        if len(header) > 0:
            out += deco.print_header_r(header) + "\n"

        out += u_KeyInput.return_screen_prt_h(options, start_at) + "\n\n"

        if invalid:
            temp_input.clear()
            invalid = False
            out += f"{colors.red}Invalid number, please pick a number from 1 to {index_class.limit}{colors.reset}"

        if temp_input.size != 0:
            out += "Action: " + str(temp_input.text())

        n_print(out)
        key = get_key()

        if key.val in u_KeyInput.current_keyboard_layout:
            val = u_KeyInput.current_keyboard_layout[key.val]
            if 0 < val <= index_class.limit:
                return val - 1
            else:
                invalid = True
            continue
        if key.is_special_char:
            if key.pressed_special_key == SpecialChar.KeyboardInterrupt:
                raise KeyboardInterrupt()
            if key.pressed_special_key == SpecialChar.Escape:
                return 0
            if key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown]:
                temp_input.clear()
                u_KeyInput.handle_arrow_key(options, key)
            elif key.pressed_special_key == SpecialChar.Backspace:
                handle_backspace(key, index_class)
            else:
                handle_f_keys(key)

        elif key.val == '\n':  # Enter key
            if temp_input.size != 0:
                selected = int(temp_input.text())
                temp_input.clear()
            else:
                selected = index_class.index
            if 0 < selected <= index_class.limit:
                return selected - 1
            else:
                invalid = True
        elif key.val in "0123456789":
            handle_number_keys(key, index_class)
            continue

        elif key.val == 'i':
            player.inventory.open_inventory()

        elif key.val == 'q':
            places.quest_logic.check_active_quests()

        elif key.val == 'h':
            u_KeyInput.display_shortcuts(True)
        elif key.val == 'o':
            u_KeyInput.change_options()