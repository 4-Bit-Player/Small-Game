import sys
from ._clipboard import get_clipboard
from ._InputClass import KeyInputIndexClass, TempInput
from ._terminal_funcs import get_key
from ._key_input import handle_arrow_key
from ._Key import SpecialChar
try:
    from printing._deco import p_red, p_reset, p_negative, toggle_ansi
    from printing import n_print
except ImportError:
    from ._fallback_printing import p_red, p_reset, p_negative, toggle_ansi, n_print



def return_screen_prt_h(lists, input_class:KeyInputIndexClass, temp_input:TempInput, recommendations:list[str]):
    recommendations = recommendations[:]
    selected = input_class.index
    lines:list[str] = []
    for line in lists:
        if isinstance(line, list):
            for l in line:
                lines.append(l)
        else:
            lines.append(line)
    if len(recommendations) != 0:
        longest = max([len(x) for x in recommendations])
        try:
            if selected != 0:
                recommendations[selected-1] = p_negative + recommendations[selected-1] + p_reset
        except IndexError:
            pass
        lines.append("~"*longest)
        lines += recommendations
        lines.append("~"*longest)
    lines.append("-->Selected: " + temp_input.text() if selected == 0 else "Selected: " + temp_input.text())

    if len(lines) == 0:
        return ""
    return "\n".join(lines)



def text_input(options: list, input_class:KeyInputIndexClass=None, forced_options=None, recommendations:list[str]=None, max_lines:int=10) -> str:
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
        recommendations = []

    curr_recommendations = recommendations
    previous_recommendations:list[list[str]] = []
    _build_lookup_table(recommendations)
    temp_input: TempInput = input_class.temp_input
    invalid = False
    input_class.index = 0
    #_start = perf_counter()
    while True:
        out = ""
        input_class.limit = min(len(curr_recommendations), max_lines)

        out += return_screen_prt_h(options, input_class, temp_input, curr_recommendations[-min(max_lines, len(curr_recommendations)):])
        if invalid:
            temp_input.clear()
            invalid = False
            out += f"\n{p_red}Invalider Input! Please pick one of the valid options.{p_reset}"
        n_print(out)
        key = get_key()

        if key.is_special_char:
            if key.pressed_special_key == SpecialChar.KeyboardInterrupt:
                raise KeyboardInterrupt()
            if key.pressed_special_key == SpecialChar.Escape:
                return "\r"

            if key.pressed_special_key in [SpecialChar.ArrowUp, SpecialChar.ArrowDown]:
                handle_arrow_key(key, input_class)
                continue

            if key.pressed_special_key == SpecialChar.Backspace:
                if key.ctrl_pressed:
                    temp_input.clear()
                    curr_recommendations = recommendations
                    previous_recommendations.clear()
                    continue
                if temp_input:
                    temp_input.rm_last_char()
                    if previous_recommendations:
                        curr_recommendations = previous_recommendations.pop()
                    else:
                        curr_recommendations = recommendations
                continue

            continue

        if key.val == '\n':  # Enter key
            if input_class.index == 0:
                selected = temp_input.text()
                temp_input.clear()
            else:
                selected = curr_recommendations[-(input_class.limit-input_class.index+1)]
            if forced_options is None:
                return selected
            else:
                if selected in forced_options:
                    return selected
                invalid = True


        elif key.val == '\x16' or key.val == '\x19': # ctrl + v or ctrl + y
             curr_recommendations = _get_clipboard_content(temp_input, curr_recommendations, previous_recommendations)
        elif key == '\x05': # ctrl+e
            toggle_ansi()

        else:
            char = key.val
            if char in _special_char_lookup:
                char = _special_char_lookup[char]
            if temp_input:
                previous_recommendations.append(curr_recommendations)
            curr_recommendations = _build_table(temp_input, char, curr_recommendations)
            temp_input += char
            input_class.index = 0
    return ""
if sys.platform == "win32":
    _special_char_lookup = {
    '\x84': "ä",
    '\x8e': "Ä",
    '\x81': "ü",
    '\x9a': "Ü",
    '\x94': "ö",
    '\x99': "Ö",
    }
else:
    _special_char_lookup = {
        '\xc3\xbc': "ü",
        '\xc3\x9c': "Ü",
        '\xc3\xa4': "ä",
        '\xc3\x84': "Ä",
        '\xc3\xb6': "ö",
        '\xc3\x96': "Ö",
    }


def _build_table(past_input:TempInput, new_key:str, options:list[str]) -> list[str]:
    upper_full_input = (past_input + new_key).text()
    lower_full_input = upper_full_input.lower()
    lower_input_parts = [x.lower() for x in lower_full_input.split(" ")]
    #print("~"+str(lower_input_parts)+"~")
    #wait_for_keypress()
    #print(lower_input_parts)
    new_options:list[list[str|int]] = []
    values = [[x, 0] for x in options]
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


_lookup_table = {}
def _build_lookup_table(options:list[str]):
    _lookup_table.clear()
    for name in options:
        _lookup_table[name] = [x.lower() for x in name.split(" ")]


def _get_clipboard_content(temp_input:TempInput, curr_recommendations:list[str], previous_recommendations:list[list[str]]):
    text = get_clipboard().strip()
    for char in text:
        curr_recommendations = _build_table(temp_input, char, curr_recommendations)
        if temp_input:
            previous_recommendations.append(curr_recommendations)
        temp_input += char
    return curr_recommendations




