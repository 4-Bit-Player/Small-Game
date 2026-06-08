from ._InputClass import KeyInputIndexClass, TempInput
from ._terminal_funcs import get_key
from ._Key import Key, SpecialChar
try:
    from printing._deco import toggle_ansi, p_negative, p_reset, p_red
    from printing import n_print

except ImportError:
    from ._fallback_printing import n_print, p_red, p_reset, p_negative, toggle_ansi

def handle_arrow_key(key:Key, input_class:KeyInputIndexClass):
    sel_col = input_class.index
    # Handle arrow key events
    if key.pressed_special_key == SpecialChar.ArrowUp:
        sel_col = sel_col - 1 if sel_col - 1 >= 1 else input_class.limit
    elif key.pressed_special_key == SpecialChar.ArrowDown:
        sel_col = sel_col + 1 if sel_col + 1 <= input_class.limit else 1
    input_class.index = sel_col


def return_screen_prt_h(options, index_class:KeyInputIndexClass, start=1):
    num = start
    selected = index_class.index
    lines:list[str] = []
    for line in options:
        if isinstance(line, list):
            if len(line) == 0:
                continue
            if line[0] == 1:
                for l in line[1:]:
                    if num == selected:
                        l_line = f"{p_negative}{num}. {l}{p_reset}"
                    else:
                        l_line = f"{num}. {l}"
                    num += 1
                    lines.append(str(l_line))
            else:
                for l in line:
                    lines.append(str(l))

        else:
            if num == selected:
                l_line = f"{p_negative}{num}. {line}{p_reset}"
            else:
                l_line = f"{num}. {line}"
            num += 1
            lines.append(str(l_line))
    if len(lines) == 0:
        return ""
    return "\n".join(lines)


def create_index(options, input_class:KeyInputIndexClass):
    limit = 0
    for line in options:
        if isinstance(line, list):
            if len(line) == 0:
                continue
            if line[0] == 1:
                limit += len(line) - 1
            continue
        else:
            limit += 1
    input_class.limit = limit
    if input_class.index > limit:
        input_class.index = limit



def wait_for_keypress() -> None:
    get_key()

def print_info_message(msg:str) -> None:
    new_lines = 1 + msg.endswith("\n")
    n_print(msg + ("\n" * new_lines)  + "(Press any key to continue)")
    wait_for_keypress()



def num_input(header:str, min_num:int|None=None, max_num:int|None=None, whole_number:bool=True, escape_allowed:bool=True) -> int|float|None:
    """
    :param header: The header
    :param min_num: The inclusive minimum number
    :param max_num: Inclusive maximum number
    :param whole_number: If it should be an int or float
    :param escape_allowed: If the escape key is allowed it will return None if it is empty or esc got pressed.
    :return:
    """
    tmp = TempInput()
    output = [
        header,
        "Error msg",
        "Number:"
    ]
    invalid:bool = False
    invalid_message:str = ""
    while True:
        output[-1] = "Number: " + tmp.text()
        if invalid:
            output[-2] = invalid_message
        else:
            output[-2] = ""

        n_print("\n".join(output))
        key = get_key(blocking=True)
        if key.is_special_char:
            if key.pressed_special_key == SpecialChar.Escape:
                if escape_allowed:
                    return None
                invalid = True
                invalid_message = p_red + "A number is required." + p_reset
                continue
            if key.pressed_special_key == SpecialChar.Backspace:  # backspace
                if key.ctrl_pressed:
                    tmp.clear()
                    continue
                if tmp:
                    tmp.rm_last_char()
                continue
            continue

        if key.val == "\n":
            txt = tmp.text()
            if len(txt) == 0:
                if escape_allowed:
                    return None
                invalid = True
                invalid_message = p_red + "A number is required." + p_reset
                continue
            num = int(txt) if whole_number else float(txt)
            if max_num is not None:
                if num > max_num:
                    invalid_message = p_red + f"Invalid number! Please select one below or equal to {max_num}." + p_reset
                    invalid = True
                    continue
            if min_num is not None:
                if num < min_num:
                    invalid_message = p_red + f"Invalid number! Please select one above or equal to {min_num}." + p_reset
                    invalid = True
                    continue
            return num

        if key.val in ".,":
            if whole_number:
                continue
            char = "."
            if char in tmp.text():
                continue
            tmp += char
            continue

        if key.val in "0123456789":
            tmp += key.val
            continue

        if key.val == "-":
            if min_num is not None and min_num >= 0:
                continue
            # I know this is not optimal, but I don't want to completely change the temp input class right now.
            # And also don't want to completely disrespect their private vars.
            lst = tmp.input_list
            tmp.clear()
            if len(lst) > 0:
                if lst[0] == "-":
                    for char in lst[1:]:
                        tmp += char
                    continue
            tmp += "-"
            for char in lst:
                tmp += char
            continue

        if key == b'\x05': # ctrl+e
            toggle_ansi()


def key_input(options: list, input_class:KeyInputIndexClass=None, start_number=1, escape_key_allowed=True) -> int:
    """
    Small main input function.

    Only allows integers as input and returns the picked option as int.

    Displays options starting from start number. (Default 1)

    Returns the selected number, starting at start number -1. (Default 0)

    :param options: The options in a list. Strings are seen as option, others are not.
    Special case: If the first item of the list is the integer 1 it will see th rest of the list as options.

    :param input_class: The input class to keep track of the input and selected option.

    :param start_number: The displayed starting number.
    :param escape_key_allowed: If set to True pressing the escape key returns start_number - 2. (default: -1)
    :return: Returns the selected number. Starting at start_number - 1
    """
    if input_class is None:
        input_class = KeyInputIndexClass()
    temp_input: TempInput = input_class.temp_input
    create_index(options, input_class)
    invalid = False

    while True:
        out = return_screen_prt_h(options, input_class, start_number) + "\n\n"
        if invalid:
            temp_input.clear()
            invalid = False
            out += f"{p_red}Invalid number, please pick a number from 1 to {input_class.limit}{p_reset}"

        if temp_input:
            out += "Action: " + str(temp_input)
        n_print(out)
        key = get_key()

        if key.is_special_char:
            if key.pressed_special_key == SpecialChar.KeyboardInterrupt:
                raise KeyboardInterrupt()

            if key.pressed_special_key == SpecialChar.Escape:
                if escape_key_allowed:
                    return start_number - 2
                continue

            if key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown] :  # Arrow keys
                temp_input.clear()
                handle_arrow_key(key, input_class)
                continue
            if key.pressed_special_key == SpecialChar.Backspace:
                handle_backspace(input_class, key)
                continue
            continue
        if key.val == '\n':  # Enter key
            if temp_input:
                selected = int(temp_input.text())
                temp_input.clear()
            else:
                selected = input_class.index
            if 0 < selected <= input_class.limit:
                return selected - 1
            else:
                invalid = True
            continue
        if key.val in "0123456789":  # number keys
            handle_num_keys(input_class, key)
            continue

        elif key.val == '\x05': # ctrl+e
            toggle_ansi()
    return 0

def handle_num_keys(input_class:KeyInputIndexClass, key:Key) -> None:
    input_class.temp_input += key.val
    num = int(input_class.temp_input.text())
    if 0 <= num <= input_class.limit:
        input_class.index = num


def handle_backspace(input_class:KeyInputIndexClass, key:Key) -> None:
    if key.pressed_special_key != SpecialChar.Backspace:
        return
    tmp_input = input_class.temp_input
    if key.ctrl_pressed:
        tmp_input.clear()
        return
    if not tmp_input:
        return
    tmp_input.rm_last_char()
    if not tmp_input:
        return
    try:
        num = int(input_class.temp_input.text())
    except ValueError:
        return
    if 0 <= num <= input_class.limit:
        input_class.index = num

def key_input_non_blocking(index_class:KeyInputIndexClass) -> int:
    """
    :return: Returns the selected number or -1 if nothing got selected.
    """

    key = get_key(blocking=False)
    temp_input: TempInput = index_class.temp_input

    if index_class.invalid:
        temp_input.clear()
        index_class.invalid = False
    if not key.is_special_char and not key.val:
        return -1
    if key.is_special_char:
        if key.pressed_special_key == SpecialChar.KeyboardInterrupt:
            raise KeyboardInterrupt()

        if key.pressed_special_key == SpecialChar.Escape:
            return 0
        if key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown]:  # Arrow keys
            temp_input.clear()
            handle_arrow_key(key, index_class)
            return -1
        if key.pressed_special_key == SpecialChar.Backspace:
            handle_backspace(index_class, key)
            return -1
        return -1
    if key.val == '\n':  # Enter key
        if temp_input.size != 0:
            selected = int(temp_input.text())
            temp_input.clear()
        else:
            selected = index_class.index
        if 0 < selected <= index_class.limit:
            return selected - 1
        else:
            index_class.invalid = True
        return -1

    if key.val in "0123456789":  # number keys
        handle_num_keys(index_class, key)
        return -1
    return -1