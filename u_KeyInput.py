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


def screen_prt_h(lists, start=1):
    num = start
    selected = lists[0][1]
    lines = []
    for line in lists:
        if line[0] == "index":
            continue

        if isinstance(line, list):
            if line[0] == 1:
                for l in line:
                    if l == 1:
                        continue
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

    for line in lines:
        print(line)
#         else:
#             print(str(start) + ". " + str(line))
#             start += 1


def create_index(options):
    limit = 0
    for line in options:
        if type(line) is list:
            if line[0] == 1:
                for i in line:
                    if i != 1:
                        limit += 1
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


def keyinput(options: list, header: list = None, start_at=1, hud=0, vertical=0):
    options = create_index(options)

    temp_input: str = ""
    # os.system('cls')
    invalid = 0

    while True:
        os.system('cls')
        if hud:
            print()
            deco.player_hud()
            print("\n")
        if header:
            for line in header:
                print(line)
        screen_prt_h(options, start_at)
        if invalid:
            deco.clear_l()
            temp_input = ""
            print(f"{colors.red}Invalid number, please pick a number from 1 to {options[0][5]}{colors.reset}")
        if temp_input:
            sys.stdout.write("Action:"+str(temp_input))
            sys.stdout.flush()
        key = msvcrt.getch()
        if key == b'\x1b':  # Escape key
            break
        elif key == b'\xe0':  # Arrow keys
            temp_input = ""
            handle_arrow_key(options)
        elif key == b'\r':  # Enter key
            if temp_input:
                selected = temp_input
            else:
                selected = options[0][1]
            if int(selected) in range(1, options[0][5]+1):
                return int(selected) - 1
            else:
                invalid = 1
        elif key in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:
            key = key.decode()
            if not temp_input:
                temp_input += key
            else:
                temp_input += key
            pass
        elif key == b'\x08':
            if temp_input:
                temp_input = temp_input[:-1]
        else:
            print(key)




# index = [
#     "index", 101,
#     "persistent", 0]

# l_stuff = [1, "Apple"]
# r_stuff = [0, f"{colors.red}▬{colors.reset}"*10]
# w_stuff = [1, "Enemy1", "Enemy2", "Enemy3", ]
# listed_stuff = [index, r_stuff, l_stuff,  r_stuff, w_stuff, r_stuff, w_stuff, ]

