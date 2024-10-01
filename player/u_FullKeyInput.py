import msvcrt
import places.quest_logic
import player.inventory
from player import u_KeyInput
from decoration import colors, deco
import os
import sys


def keyinput(options: list, header: str = None, start_at=1, hud: bool = False):
    options = u_KeyInput.create_index(options)

    temp_input: str = ""
    os.system('cls')

    invalid = False
    if hud:
        tmp = [deco.player_hud(False) + "\n"]
        if options[0][0] == "index":
            options.insert(1, tmp)
            if header:
                options.insert(2,[deco.print_header_r(header)])
        else:
            options.insert(0, tmp)
            if header:
                options.insert(1,[deco.print_header_r(header)])

    elif header:
        tmp = [deco.print_header_r(header)]
        if options[0][0] == "index":
            options.insert(1, tmp)
        else:
            options.insert(0, tmp)

    lines_to_remove = 15 + len(options)

    while True:
        out = u_KeyInput.return_screen_prt_h(options, start_at) + "\n\n"

        if invalid:
            temp_input = ""
            invalid = False
            out += f"{colors.red}Invalid number, please pick a number from 1 to {options[0][5]}{colors.reset}"

        if temp_input:
            out += "Action: " + str(temp_input)

        #print(out, end="")
        sys.stdout.write(out)
        sys.stdout.flush()
        key = msvcrt.getch()
        deco.clear_screen(lines_to_remove)

        if key in u_KeyInput.current_keyboard_layout:
            val = u_KeyInput.current_keyboard_layout[key]
            if 0 < val <= options[0][5] + 1:
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
            if 0 < int(selected) <= options[0][5] + 1:
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

        else:
            print(key)
            os.system('cls')

# index = [
#     "index", 101,
#     "persistent", 0]

# l_stuff = [1, "Apple"]
# r_stuff = [0, f"{colors.red}▬{colors.reset}"*10]
# w_stuff = [1, "Enemy1", "Enemy2", "Enemy3", ]
# listed_stuff = [index, r_stuff, l_stuff,  r_stuff, w_stuff, r_stuff, w_stuff, ]


