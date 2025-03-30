import time
from decoration import colors, deco
from printing.print_queue import n_print
from printing import print_queue
from player import user, cheats
import sys

if sys.platform == "win32":
    from msvcrt import getch
else:
    import readchar
    _char_buffer = b''
    _arrow_keys = [ b'\x1b[B',b'\x1b[A', b'\x1b[C', b'\x1b[D']
    _f_keys = {b'\x1b0P', b'\x1b0Q', b'\x1b0R', b'\x1b0S', b'\x1b[15~', b'\x1b[17~', b'\x1b[18~', b'\x1b[19~', b'\x1b[20~', b'\x1b[21~'}
    _char_lookup = {
        b'\n': b'\r',
        b'\x1b[B': b'P',   # arrow down
        b'\x1b[A': b'H',  # Up arrow key
        b'\x1b[C': b'M',  # Right arrow key
        b'\x1b[D': b'K',  # Left arrow key
        b'\xc2\xa7': b'\xf5', # shift+3 german layout
        b'\x1b\x1b': b'\x1b', # escape key
        b'\x7f': b'\x08', # backspace
        b'\x1b0P': b';', # F1
        b'\x1b0Q': b'<', # F2
        b'\x1b0R': b'=', # F3
        b'\x1b0S': b'>', # F4
        b'\x1b[15~': b'?', # F5
        b'\x1b[17~': b'@', # F6
        b'\x1b[18~': b'A', # F7
        b'\x1b[19~': b'B', # F8
        b'\x1b[20~': b'C', # F9
        b'\x1b[21~': b'D', # F10

    }
    def getch():
        global _char_buffer
        if _char_buffer != b'':
            if _char_buffer in _char_lookup:
                char = _char_lookup[_char_buffer]
                _char_buffer = b''
                return char
            _char_buffer = b''
        char = readchar.readkey().encode()
        if char in _arrow_keys: # arrow keys
            _char_buffer = char
            return b'\xe0'
        if char in _f_keys:
            _char_buffer = char
            return b'\00'


        if char in _char_lookup:
            return _char_lookup[char]
        return char


def _get_char():
    return getch()

options_open = True


def toggle_ui_centered():
    user.settings["centered_screen"] = not user.settings["centered_screen"]

def change_options():
    global options_open
    if options_open:
        return
    options_open = True
    options = [["index",1,0,0,0,0]]
    while True:
        options = [options[0],
            ["What would you like to change?\n"],
            "Nothing (Return)",
            "Toggle Ui (centered/left sided)",
            f"Keyboard layout (current layout: {current_keyboard_layout['layout_name']})",
            f"Change your name (current name: {user.Player['name']})",
            "Close the Game",
        ]
        if sys.path[0].endswith(r"\Python\Small Game"):
            options += [
                f"Cheat Menu",
                f"Toggle test setting (currently: {user.test})",
                f"Toggle constant refresh (currently: {print_queue._constant_refresh})",
                f"Toggle fps (currently: {print_queue._show_fps})",
            ]

        pick = keyinput(options, header="Options")
        if pick == 0:
            options_open = False
            return
        if pick == 1:
            toggle_ui_centered()
        elif pick == 2:
            keyboard_layout_init()
        elif pick == 3:
            name_init()
        elif pick == 4:
            if user_confirmation("close the game"):
                exit_game()
        elif pick == len(options)-6:
            cheats.cheat_menu()
        elif pick == len(options)-5:
            user.toggle_test()
        elif pick == len(options)-4:
            print_queue.toggle_constant_refresh()
        elif pick == len(options)-3:
            print_queue.toggle_fps()


def user_confirmation(stuff_to_confirm:str):
    pick = keyinput([[f"Are you sure that you want to {stuff_to_confirm}?"], "No", "Yes"])
    if pick == 0:
        return False
    return True






# def handle_arrow_key_vert(sel_list):
#     selected = sel_list[0][1]
#     sel_row = int(str(selected)[0])
#     sel_col = int(str(selected)[1:])
#
#     # Handle arrow key events
#     key = msvcrt.getch()
#     if key == b'H':  # Up arrow key
#         sel_col = sel_col - 1 if sel_col - 1 >= 1 else 1
#
#     elif key == b'P':  # Down arrow key
#         sel_col = sel_col + 1 if sel_col + 1 < len(sel_list[sel_row]) else len(sel_list[sel_row]) - 1
#
#     elif key == b'M':  # Right arrow key
#         sel_row = sel_row + 1 if not sel_row + 1 > len(sel_list) - 1 else len(sel_list) - 1
#         while not sel_list[sel_row][0]:
#             sel_row = sel_row + 1 if not sel_row + 1 > len(sel_list) - 1 else int(str(selected)[0])
#
#         if sel_col >= len(sel_list[sel_row]):
#             sel_col = len(sel_list[sel_row]) - 1
#         elif sel_col < 1:
#             sel_col = 1
#
#     elif key == b'K':  # Left arrow key
#         sel_row = sel_row - 1 if not sel_row - 1 < 1 else 1
#         while not sel_list[sel_row][0]:
#             if not sel_row - 1 == 0:
#                 sel_row = sel_row - 1
#             elif sel_row - 1 == 0:
#                 sel_row = int(str(selected)[0])
#                 break
#
#         if sel_col >= len(sel_list[sel_row]):
#             sel_col = len(sel_list[sel_row]) - 1
#         elif sel_col < 1:
#             sel_col = 1
#
#     sel_list[0][1] = sel_row * 100 + sel_col


def handle_arrow_key(sel_list):
    sel_col = sel_list[0][1]

    # Handle arrow key events
    key = _get_char()
    if key == b'H':  # Up arrow key
        sel_col = sel_col - 1 if sel_col - 1 >= 1 else sel_list[0][5]

    elif key == b'P':  # Down arrow key
        sel_col = sel_col + 1 if sel_col + 1 <= sel_list[0][5] else 1

    # elif key == b'M':  # Right arrow key
    #     sel_row = sel_row + 1 if not sel_row + 1 > len(sel_list) - 1 else len(sel_list) - 1
    #     while not sel_list[sel_row][0]:
    #         sel_row = sel_row + 1 if not sel_row + 1 > len(sel_list) - 1 else int(str(selected)[0])
    #
    #     if sel_col >= len(sel_list[sel_row]):
    #         sel_col = len(sel_list[sel_row]) - 1
    #     elif sel_col < 1:
    #         sel_col = 1

    # elif key == b'K':  # Left arrow key
    #     sel_row = sel_row - 1 if not sel_row - 1 < 1 else 1
    #     while not sel_list[sel_row][0]:
    #         if not sel_row - 1 == 0:
    #             sel_row = sel_row - 1
    #         elif sel_row - 1 == 0:
    #             sel_row = int(str(selected)[0])
    #             break
    #
    #     if sel_col >= len(sel_list[sel_row]):
    #         sel_col = len(sel_list[sel_row]) - 1
    #     elif sel_col < 1:
    #         sel_col = 1

    sel_list[0][1] = sel_col


current_keyboard_layout = {}

german_layout = {
    b'!': 1,
    b'"': 2,
    b'\xf5': 3,
    b'$': 4,
    b'%': 5,
    b'&': 6,
    b'/': 7,
    b'(': 8,
    b')': 9,
    "layout_name":"german"
}
english_layout = {
    b'!': 1,
    b'@': 2,
    b'#': 3,
    b'$': 4,
    b'%': 5,
    b'^': 6,
    b'&': 7,
    b'*': 8,
    b'(': 9,
    "layout_name":"english"
}


def name_init():
    n_print("\nPlease enter your name:")
    #time.sleep(0.02) # input() blocks the print function. sleeping so the print function can render it at least once correctly.
    user.Player["name"] = user.Player_default["name"] = input()

def keyboard_layout_init():
    global current_keyboard_layout
    n_print("What keyboard are you using?\n"
                "Type 'e' if you are using the english layout,\n"
                "or anything else if you are using the german layout.\n"
                "(It's just for number hotkeys)\n"
                "Keyboard Layout: ")

    if input().lower() == "e":
        current_keyboard_layout = english_layout
    else:
        current_keyboard_layout = german_layout


def return_screen_prt_h(lists, start=1):
    num = start
    selected = 0
    lines:list[str] = []
    for line in lists:
        if line[0] == "index":
            selected = lists[0][1]
            continue

        if isinstance(line, list):
            if line[0] == 1:
                for l in line[1:]:
                    if num == selected:
                        l_line = colors.negative + str(num) + ". " + str(l) + " " + colors.reset
                    else:
                        l_line = (str(num) + ". " + str(l))
                    num += 1
                    lines.append(l_line)
            else:
                for l in line:
                    lines.append(l)

        else:
            if num == selected:
                l_line = colors.negative + str(num) + ". " + str(line) + " " + colors.reset
            else:
                l_line = (str(num) + ". " + str(line))
            num += 1
            lines.append(l_line)
    if len(lines) == 0:
        return ""
    return "\n".join(lines)


def create_index(options):
    limit = 0
    for line in options:
        if isinstance(line, list):
            if line[0] == 1:
                limit += len(line) - 1
            continue
        else:
            limit += 1
    if options[0][0] == "index":
        options[0][5] = limit
        if options[0][1] > limit:
            options[0][1] = limit
    else:
        index = [
            "index", 1,
            "persistent", 1,
            "limit", limit]
        options.insert(0, index)
    return options


def display_shortcuts(full=False):
    out = deco.print_header_r("Shortcuts", "~") + "\n"
    if full:
        out += (
            "i = open inventory\n"
            "q = view active quests\n"
            )
    out += ("h = open the available shortcuts\n"
            "o = change options\n"
            "esc = pick the first option (usually going back, unless in fights)\n"
            "shift + number key (not num pad)= instantly select an option\n"
            "ctrl + c = crash the game. :)\n\n"
            "Press enter to return")
    n_print(out)
    wait_for_keypress()


def wait_for_keypress():
    _get_char()


def keyinput(options: list, header: str = None, start_at=1, hud: bool = False):
    options = create_index(options)

    temp_input: str = ""
    invalid = False

    while True:
        out = ""
        if hud:
            out += deco.player_hud() + "\n\n"
        if header:
            out += deco.print_header_r(header) + "\n"
        out += return_screen_prt_h(options, start_at) + "\n\n"
        if invalid:
            temp_input = ""
            invalid = False
            out += f"{colors.red}Invalid number, please pick a number from 1 to {options[0][5]}{colors.reset}"

        if temp_input:
            out += "Action: " + str(temp_input)
        n_print(out)
        key = _get_char()

        if key in current_keyboard_layout:
            val = current_keyboard_layout[key]
            if 0 < val <= options[0][5]:
                return val - 1
            else:
                invalid = True
            continue

        if key == b'\x1b':  # Escape key
            return 0
        elif key == b'\xe0':  # Arrow keys
            temp_input = ""
            handle_arrow_key(options)
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
        elif key == b'h':
            display_shortcuts(False)
        elif key == b'o':
            change_options()
        elif key == b'\x00':
            handle_f_keys()
        else:
            print(key)



def handle_f_keys():
    char = _get_char()
    if char == b';': # F1
        pass
    elif char == b'<': # F2
        pass
    elif char == b'=': # F3
        pass
    elif char == b'>': # F4
        pass
    elif char == b'?': # F5
        print_queue.toggle_constant_refresh()
    elif char == b'@': # F6
        print_queue.toggle_fps()
    elif char == b'A': # F7
        change_fps()
    elif char == b'B': # F8
        pass
    elif char == b'C': # F9
        pass
    elif char == b'D': # F10
        pass
    else:
        print("f? ",  char)


def exit_game():
    deco.full_clear()
    exit()

def change_fps():
    with print_queue.TemporaryDisablePrintUpdates() as _:
        invalid = True
        try:
            n_print("\nWhat should be the new fps limit?\n")
            new_limit = float(input("Limit: "))
            if 1_000_001 > new_limit > 0:
                invalid = False
                print_queue.change_fps_limit(new_limit)
        except ValueError:
            pass
        if invalid:
            n_print("\nInvalid input")
            time.sleep(0.5)