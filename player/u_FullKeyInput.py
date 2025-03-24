import msvcrt
import places.quest_logic
import player.inventory
from player import u_KeyInput
from decoration import colors, deco
from printing.print_queue import n_print


def keyinputfull(options: list, header: str = "", start_at=1, hud: bool = False):
    options = u_KeyInput.create_index(options)

    temp_input: str = ""

    invalid = False

    while True:
        out = ""
        if hud:
            out += deco.player_hud() + "\n"
        if len(header) > 0:
            out += deco.print_header_r(header) + "\n"

        out += u_KeyInput.return_screen_prt_h(options, start_at) + "\n\n"

        if invalid:
            temp_input = ""
            invalid = False
            out += f"{colors.red}Invalid number, please pick a number from 1 to {options[0][5]}{colors.reset}"

        if temp_input:
            out += "Action: " + str(temp_input)

        n_print(out)
        key = msvcrt.getch()

        if key in u_KeyInput.current_keyboard_layout:
            val = u_KeyInput.current_keyboard_layout[key]
            if 0 < val <= options[0][5]:
                return val - 1
            else:
                invalid = True
            continue

        if key == b'\x1b':  # Escape key
            return 0
        elif key == b'\xe0':  # Arrow keys
            temp_input = ""
            u_KeyInput.handle_arrow_key(options)

        elif key == b'\r':  # Enter key
            if temp_input:
                selected = temp_input
            else:
                selected = options[0][1]
            if 0 < int(selected) <= options[0][5]:
                return int(selected) - 1
            else:
                invalid = True
        elif key in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:  # number keys
            key = key.decode()
            if not temp_input:
                temp_input += key
            else:
                temp_input += key
            pass
        elif key == b'\x08':  # backspace
            if temp_input:
                temp_input = temp_input[:-1]

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


