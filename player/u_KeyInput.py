import msvcrt
from decoration import colors, deco
import os
import sys


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
    key = msvcrt.getch()
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
}


def keyboard_layout_init():
    global current_keyboard_layout
    os.system('cls')
    tmp = input("What keyboard are you using?\n"
                "Type 'e' if you are using the english layout,\n"
                "or anything else if you are using the german layout.\n"
                "(It's just for num hotkeys)\n"
                "Keyboard Layout: ")
    if tmp == "e":
        current_keyboard_layout = english_layout
    else:
        current_keyboard_layout = german_layout



def return_screen_prt_h(lists, start=1):
    num = start
    selected = 0
    lines = []
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
    os.system('cls')
    out = deco.print_header_r("Shortcuts", "~") + "\n"
    if full:
        out += ("i = open inventory\n"
                "q = view active quests\n")
    out += ("h = open the available shortcuts\n"
            "esc = pick the first option (usually going back, unless in fights)\n"
            "shift + num key = instantly select an option\n"
            "ctrl + c (or ctrl + 2 for some reason) = crash the game. :)\n\n"
            "Press enter to return")

    wait_for_keypress()

def wait_for_keypress():
    msvcrt.getch()


def keyinput(options: list, header: str = None, start_at=1, hud: bool = False):
    options = create_index(options)

    temp_input: str = ""
    # os.system('cls')
    invalid = False



    while True:
        os.system('cls')
        if hud:
            sys.stdout.write(deco.player_hud(False) + "\n\n")
        if header:
            sys.stdout.write(deco.print_header_r(header) + "\n")
        print(return_screen_prt_h(options, start_at))
        if invalid:
            #deco.clear_l()
            temp_input = ""
            print(f"{colors.red}Invalid number, please pick a number from 1 to {options[0][5]}{colors.reset}")
        if temp_input:
            sys.stdout.write("Action:"+str(temp_input))
        sys.stdout.flush()
        key = msvcrt.getch()
        os.system('cls')

        if key in current_keyboard_layout:
            val = current_keyboard_layout[key]
            if 0 < val <= options[0][5] + 1:
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
            if 0 < int(selected) <= options[0][5]+1:
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
        else:
            print(key)




# index = [
#     "index", 101,
#     "persistent", 0]

# l_stuff = [1, "Apple"]
# r_stuff = [0, f"{colors.red}▬{colors.reset}"*10]
# w_stuff = [1, "Enemy1", "Enemy2", "Enemy3", ]
# listed_stuff = [index, r_stuff, l_stuff,  r_stuff, w_stuff, r_stuff, w_stuff, ]


