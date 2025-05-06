import places.quest_logic
import player.inventory
from player import u_KeyInput
from decoration import colors, deco
from player.keyinput_index_class import KeyinputIndexClass, TempInput
from player.u_KeyInput import handle_number_keys, handle_backspace
from printing.print_queue import n_print


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
        key = u_KeyInput.get_char()

        if key in u_KeyInput.current_keyboard_layout:
            val = u_KeyInput.current_keyboard_layout[key]
            if 0 < val <= index_class.limit:
                return val - 1
            else:
                invalid = True
            continue

        if key == b'\x1b':  # Escape key
            return 0
        elif key == b'\xe0':  # Arrow keys
            temp_input.clear()
            u_KeyInput.handle_arrow_key(options)

        elif key == b'\r':  # Enter key
            if temp_input.size != 0:
                selected = int(temp_input.text())
                temp_input.clear()
            else:
                selected = index_class.index
            if 0 < selected <= index_class.limit:
                return selected - 1
            else:
                invalid = True
        elif key in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:  # number keys
            handle_number_keys(key, index_class)
            continue
        elif key == b'\x7f' or key == b'\x08':  # (ctrl+) backspace
            if temp_input.size != 0:
                handle_backspace(key, index_class)

        elif key == b'\x03':  # ctrl + c
            raise KeyboardInterrupt

        elif key == b'i':
            player.inventory.open_inventory()

        elif key == b'q':
            places.quest_logic.check_active_quests()

        elif key == b'h':
            u_KeyInput.display_shortcuts(True)
        elif key == b'\x00':
            u_KeyInput.handle_f_keys()
        elif key == b'o':
            u_KeyInput.change_options()

        else:
            print(key)
            #os.system('cls')

# index = [
#     "index", 101,
#     "persistent", 0]

# l_stuff = [1, "Apple"]
# r_stuff = [0, f"{colors.red}▬{colors.reset}"*10]
# w_stuff = [1, "Enemy1", "Enemy2", "Enemy3", ]
# listed_stuff = [index, r_stuff, l_stuff,  r_stuff, w_stuff, r_stuff, w_stuff, ]


