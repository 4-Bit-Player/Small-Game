from time import sleep
from decoration import colors, deco
from player.keyinput_index_class import KeyinputIndexClass, TempInput, LAClass
from printing import n_print, toggle_constant_refresh, toggle_fps, change_fps_limit, TemporaryDisablePrintUpdates, \
    toggle_centered_text, get_header, full_clear, n_exit
from printing import _print_queue
from player import user, cheats
from input_system import get_key, input as legacy_input, text_input, SpecialChar, Key, stop_keyboard_input, num_input, wait_for_keypress
import sys


options_open = True


def toggle_ui_centered():
    user.settings["centered_screen"] = not user.settings["centered_screen"]
    toggle_centered_text()

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
                f"Toggle constant refresh (currently: {_print_queue._constant_refresh})",
                f"Toggle fps (currently: {_print_queue._show_fps})",
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
            toggle_constant_refresh()
        elif pick == len(options)-3:
            toggle_fps()


def user_confirmation(stuff_to_confirm:str) -> bool:
    """
    are you sure that you want to {stuff_to_confirm}?
    :param stuff_to_confirm: stuff to confirm
    :return: Bool if they are sure or not
    """
    pick = keyinput([[f"Are you sure that you want to {stuff_to_confirm}?"], "No", "Yes"])
    if pick == 0:
        return False
    return True





def handle_arrow_key(sel_list, key:Key):
    sel_col = sel_list[0].index

    if key.pressed_special_key == SpecialChar.ArrowUp:
        sel_col = sel_col - 1 if sel_col - 1 >= 1 else sel_list[0].limit
    elif key.pressed_special_key == SpecialChar.ArrowDown:
        sel_col = sel_col + 1 if sel_col + 1 <= sel_list[0].limit else 1
    sel_list[0].index = sel_col


current_keyboard_layout = {}

german_layout = {
    '!': 1,
    '"': 2,
    '\xf5': 3,
    '$': 4,
    '%': 5,
    '&': 6,
    '/': 7,
    '(': 8,
    ')': 9,
    "layout_name":"german"
}
english_layout = {
    '!': 1,
    '@': 2,
    '#': 3,
    '$': 4,
    '%': 5,
    '^': 6,
    '&': 7,
    '*': 8,
    '(': 9,
    "layout_name":"english"
}


def name_init():
    name = text_input([get_header("The Name of the Hero"), "\nPlease enter your name:"])
    user.Player["name"] = user.Player_default["name"] = name

def keyboard_layout_init():
    global current_keyboard_layout
    layout = text_input(["What keyboard are you using?\n"
                "Type 'e' if you are using the english layout,\n"
                "or anything else if you are using the german layout.\n"
                "(It's just for number hotkeys)\n"
                "Keyboard Layout: "])
    if layout.lower() == "e":
        current_keyboard_layout = english_layout
    else:
        current_keyboard_layout = german_layout


def return_screen_prt_h(lists, start=1):
    num = start
    selected = 0
    lines:list[str] = []
    if isinstance(lists[0], KeyinputIndexClass):
        selected = lists[0].index
    for line in lists:

        if isinstance(line, list):
            if len(line) == 0:
                lines.append("")
                continue
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

        if isinstance(line, str):
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
        if isinstance(line, str):
            limit += 1
            continue
        if isinstance(line, list):
            if len(line) == 0:
                continue
            if line[0] == 1:
                limit += len(line) - 1
            continue
        else:
            continue
    if isinstance(options[0], KeyinputIndexClass):
        options[0].limit = limit
        if options[0].index > limit:
            options[0].index = limit

    else:
        c = KeyinputIndexClass(1, limit, True)
        if len(options[0]) != 0 and options[0][0] == "index":
            options[0] = c
        else:
            options.insert(0, c)
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




def keyinput(options: list, header: str = None, start_at=1, hud: bool = False):
    options = create_index(options)
    index_class:KeyinputIndexClass = options[0]
    temp_input: TempInput = index_class.temp_input
    invalid = False

    while True:
        out = ""
        if hud:
            out += deco.player_hud() + "\n\n"
        if header:
            out += deco.print_header_r(header) + "\n"
        out += return_screen_prt_h(options, start_at) + "\n\n"
        if invalid:
            temp_input.clear()
            invalid = False
            out += f"{colors.red}Invalid number, please pick a number from 1 to {index_class.limit}{colors.reset}"

        if temp_input.size != 0:
            out += "Action: " + str(temp_input.text())
        n_print(out)
        key = get_key()

        if key.val in current_keyboard_layout:
            val = current_keyboard_layout[key.val]
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
            elif key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown]:
                temp_input.clear()
                handle_arrow_key(options, key)
                continue
            elif key.pressed_special_key == SpecialChar.Backspace:
                handle_backspace(key, index_class)
            else:
                handle_f_keys(key)

        elif key.val == '\n':  # Enter key
            if temp_input.size != 0:
                selected = temp_input.text()
                temp_input.clear()
            else:
                selected = index_class.index
            if 0 < int(selected) <= index_class.limit:
                return int(selected) - 1
            else:
                invalid = True
        elif key.val in "0123456789":
            handle_number_keys(key,index_class)
            continue
        elif key.val == 'h':
            display_shortcuts(False)
        elif key.val == 'o':
            change_options()




def handle_f_keys(key:Key):
    if key.pressed_special_key == SpecialChar.F5:
        toggle_constant_refresh()
    if key.pressed_special_key == SpecialChar.F6:
        toggle_fps()
    if key.pressed_special_key == SpecialChar.F7:
        change_fps()

def exit_game():
    full_clear()
    stop_keyboard_input()
    n_exit()
    exit()

def change_fps():
    invalid = True
    new_limit = num_input("\nWhat should be the new fps limit?\n"
                          "(Press escape to cancel)\n"
                          "New Limit:",
                          min_num=1,
                          max_num=1_000_000,
                          whole_number=True,
                          escape_allowed=True)
    if new_limit is None:
        return
    change_fps_limit(new_limit)


def non_blocking_keyinput(key:Key, la_class:LAClass) -> int:
    """
    :param key: last key pressed as bytes
    :param la_class: a LAClass
    :return: Returns the selected number or -1 if nothing got selected yet.
    """
    index_class: KeyinputIndexClass = la_class.index
    temp_input: TempInput = index_class.temp_input

    if index_class.invalid:
        temp_input.clear()
        index_class.invalid = False

    if key.val in current_keyboard_layout:
        val = current_keyboard_layout[key.val]
        if 0 < val <= index_class.limit:
            return val - 1
        else:
            index_class.invalid = True
        return -1
    if key.is_special_char:
        if key.pressed_special_key == SpecialChar.KeyboardInterrupt:
            raise KeyboardInterrupt()
        if key.pressed_special_key == SpecialChar.Escape:
            return 0
        if key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown]:  # Arrow keys
            temp_input.clear()
            la_class.updated = True
            handle_arrow_key([index_class], key)
        elif key.pressed_special_key == SpecialChar.Backspace:
            if temp_input.size != 0:
                handle_backspace(key, index_class)
                la_class.updated = True
        else:
            la_class.paused = True
            sleep(0.1)
            handle_f_keys(key)
            la_class.paused = False

    elif key.val == '\n':  # Enter key
        la_class.updated = True
        if temp_input.size != 0:
            selected = int(temp_input.text())
            temp_input.clear()
        else:
            selected = index_class.index
        if 0 < selected <= index_class.limit:
            return selected - 1
        else:
            index_class.invalid = True

    elif key.val in "0123456789":  # number keys
        handle_number_keys(key, la_class.index)
        la_class.updated = True
        return -1

    elif key.val == 'h':
        la_class.paused = True
        sleep(0.1)
        display_shortcuts(False)
        la_class.paused = False
    elif key.val == 'o':
        la_class.paused = True
        sleep(0.1)
        change_options()
        la_class.paused = False
    return -1


def handle_number_keys(key:Key, index_class:KeyinputIndexClass):
    val:str = key.val
    num = int(index_class.temp_input.text() + val)
    if 0 < num < index_class.limit:
        index_class.index = num
    index_class.temp_input += val

def handle_backspace(key:Key, index_class:KeyinputIndexClass):
    if index_class.temp_input.size == 0 or not key.pressed_special_key == SpecialChar.Backspace:
        return
    tmp_input = index_class.temp_input

    if key.ctrl_pressed:
        tmp_input.clear()
        index_class.index = 0
        return
    tmp_input.rm_last_char()
    if tmp_input.size == 0:
        return
    try:
        num = int(tmp_input.text())
        if 0 < num < index_class.limit:
            index_class.index = num
        return
    except ValueError:
        index_class.index = 0