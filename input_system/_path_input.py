from time import perf_counter
from ._InputClass import TempInput, KeyInputIndexClass
from ._text_input import return_screen_prt_h, handle_arrow_key, _special_char_lookup
from ._terminal_funcs import get_key
from ._clipboard import get_clipboard
from ._Key import SpecialChar
import os, string
try:
    from printing._deco import p_red, p_reset, p_negative, toggle_ansi
    from printing import n_print
except ImportError:
    from ._fallback_printing import p_red, p_reset, p_negative, toggle_ansi, n_print



def _get_clipboard_content(temp_input:TempInput, curr_recommendations:list[str], previous_recommendations:list[list[str]]):
    text = get_clipboard().strip()
    for char in text:
        curr_recommendations = _build_path_table(temp_input, char, curr_recommendations)
        #if temp_input:
        #    previous_recommendations.append(curr_recommendations)
        temp_input += char

    return curr_recommendations




def path_input(options: list, input_class:KeyInputIndexClass=None, forced_options=None, recommendations:list[str]=None, max_lines:int=10) -> str:
    """

    :param options:
    :param forced_options: List of strings from which one has to get returned
    :param recommendations: List of recommended strings
    :param max_lines: the maximum amount of recommended lines
    :return: The input as string. Returns \r if esc was pressed
    """
    if input_class is None:
        input_class = KeyInputIndexClass()
    if recommendations is None:
        recommendations = [x for x in os.listdir(os.curdir)]

    curr_recommendations = recommendations
    previous_recommendations:list[list[str]] = []
    temp_input: TempInput = input_class.temp_input
    if "/" in os.path.abspath("."):
        split_char = "/"
    else:
        split_char = "\\"

    for x in os.path.abspath(".").split(split_char):
        temp_input += x + split_char



    invalid = False
    input_class.index = 0
    #_start = perf_counter()
    screen_time = 0
    keystrokes = 0
    key_time = 0
    other_time = 0
    end = 0
    while True:
        out = ""
        input_class.limit = min(len(curr_recommendations), max_lines)
        if keystrokes > 2:
            other_time += perf_counter() - end
        out += return_screen_prt_h(options, input_class, temp_input, curr_recommendations[-min(max_lines, len(curr_recommendations)):])
        if invalid:
            temp_input.clear()
            invalid = False
            out += f"\n{p_red}Invalider Input! Bitte trage etwas von den validen Optionen ein.{p_reset}"
        n_print(out)
        key = get_key()

        end = perf_counter()
        if key.is_special_char:
            if key.pressed_special_key == SpecialChar.KeyboardInterrupt:
                raise KeyboardInterrupt()
            if key.pressed_special_key == SpecialChar.Escape:
                return "\r"
            if key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown]:
                handle_arrow_key(key, input_class)
            if key.pressed_special_key == SpecialChar.Backspace:
                if key.ctrl_pressed:
                    temp_input.clear()
                    curr_recommendations = get_drive_paths(split_char)
                    continue
                if temp_input:
                    temp_input.rm_last_char()
                    curr_recommendations = update_recommendation(temp_input)
                continue

            continue
        val = key.val
        if val == '\n':
            if input_class.index == 0:
                selected = temp_input.text()
                temp_input.clear()

            else:
                selected = curr_recommendations[-(input_class.limit-input_class.index+1)]
                pth = temp_input.text()
                if not temp_input.text().endswith(split_char):
                    pos = pth.rfind(split_char, 0)
                    if pos != -1:
                        for _ in range(len(pth)-pos-1):
                            temp_input.rm_last_char()
                        pth = pth[:pos]

                ab_path = os.path.join(pth, selected)

                if os.path.isdir(ab_path):
                    if temp_input.size != 0:
                        temp_input += selected + split_char
                    else:
                        temp_input += selected
                    #previous_recommendations.append(curr_recommendations)

                    curr_recommendations = update_recommendation(temp_input)
                    continue
                return ab_path

            if forced_options is None:

                return selected
            else:
                if selected in forced_options:
                    return selected
                invalid = True


        elif key.val == '\x16' or key.val == '\x19': # ctrl + v or ctrl + y
             curr_recommendations = _get_clipboard_content(temp_input, curr_recommendations, previous_recommendations)
        elif val == '\x05': # ctrl+e
            toggle_ansi()

        else:
            char = val
            if char in _special_char_lookup:
                char = _special_char_lookup[char]
            else:
                if char not in string.printable:
                    continue
            curr_recommendations = _build_path_table(temp_input, char, curr_recommendations)
            temp_input += char
            input_class.index = 0
    return ""

def get_drive_paths(split_char="/") -> list[str]:
    return [f"{x}:{split_char}" for x in string.ascii_uppercase if os.path.exists(f"{x}:{split_char}")]


def update_recommendation(temp_input:TempInput) -> list[str]:
    text = temp_input.text()
    split_char = "\\" if "\\" in text else "/"
    if text == "":
        return get_drive_paths(split_char)
    if os.path.exists(text):
        return os.listdir(text)
    if os.path.exists(text[:text.rfind(split_char)]):
        return os.listdir(text[:text.rfind(split_char)])

    return []

def _build_path_table(past_input:TempInput, new_key:str, options:list[str]) -> list[str]:
    options = update_recommendation(past_input)
    actual_input = (past_input + new_key).text()
    split_char = "\\" if "\\" in actual_input else "/"
    if actual_input.rfind(split_char) != -1:
        upper_full_input = actual_input[actual_input.rfind(split_char)+1:]
    else:
        upper_full_input = actual_input
    lower_full_input = upper_full_input.lower()
    lower_input_parts = [x.lower() for x in lower_full_input.split(split_char)]
    new_options:list[list[str|int]] = []
    values = [[x, 0] for x in options]
    _lookup_table = {x:x.split(" ") for x in options}
    for i in range(len(values)):
        upper_current_item = options[i]
        lower_current_item = upper_current_item.lower()

        for i_part in range(len(lower_input_parts)):
            input_part = lower_input_parts[i_part]
            found = False
            if lower_full_input in lower_current_item:
                values[i][1] += len(upper_full_input)
                if lower_current_item.startswith(lower_full_input):
                    values[i][1] += len(upper_full_input)

                if upper_full_input in upper_current_item:
                    values[i][1] += len(upper_full_input)
                    if upper_current_item.startswith(upper_full_input):
                        values[i][1] += len(upper_full_input)
                        if upper_full_input == upper_current_item:
                            values[i][1] += 100

                found = True

            for part in _lookup_table[upper_current_item]:
                if part.find(input_part) == -1:
                    continue
                if upper_full_input in upper_current_item:
                    values[i][1] += len(upper_full_input)
                if new_key in upper_current_item:
                    values[i][1] += 1
                if part.startswith(input_part):
                    values[i][1] += len(input_part)

                found = True
                values[i][1] += len(input_part)




            if not found:
                values[i][1] -= 1000
        if values[i][1] <= 0:
            continue
        new_options.append(values[i])
    new_options.sort(key=lambda a: a[1])



    return [x[0] for x in new_options]