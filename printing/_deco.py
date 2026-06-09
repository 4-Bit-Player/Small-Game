from os import system
from sys import stdout, platform
from shutil import get_terminal_size

p_red = '\033[38;5;160m'
p_reset = '\033[0;0m'
p_green = f'\033[38;5;28m'
p_yellow = '\033[38;5;220m'
p_turquoise = '\033[38;5;48m'
p_pink = '\033[38;5;200m'
p_light_green = f'\033[38;5;34m'
p_gray = '\033[38;5;245m'
p_gold = '\033[38;5;214m'
p_light_blue = '\033[38;5;80m'
p_negative = f'\033[7;5;160m'

_line_len = 46
_use_ansi = True
_reset_console = "cls" if platform == "win32" else "clear"

def clear_screen(lines_to_remove:int=20, lines_to_remove_ahead:int=0) -> None:
    if not _use_ansi:
        system(_reset_console)
        return
    clearing_current_line = ""
    if lines_to_remove != 0:
        clearing_current_line = "\033[0G\033[K"
    stdout.write("\033[E"*lines_to_remove_ahead + clearing_current_line + "\033[F\033[K"*(lines_to_remove_ahead-1+lines_to_remove))
    return


def full_clear() -> None:
    if not _use_ansi:
        system(_reset_console)
        return
    stdout.write("\033c") # resets the console
    pass


def get_line_len() -> int:
    return _line_len


def set_line_len(char_num:int) -> None:
    global _line_len
    _line_len = char_num


def get_header(*header, char:str='~') -> str:
    header = [str(x) for x in header]
    hwidth = _line_len
    for i in range(len(header)):
        header[i] = header[i].center(hwidth) + "\n"
    return  (char * hwidth + "\n" +
              "".join(header) +
              char * hwidth + "\n")


def toggle_ansi() -> None:
    """
    Toggles if it should use ANSII escape sequences to clear the screen or system calls.
    Also replaces some ANSII sequences for highlighting lines.

    """
    global _use_ansi
    _use_ansi = not _use_ansi

def using_ansi() -> bool:
    return _use_ansi


def replace_ansi(text:str) -> str:
    out = text.replace(p_reset, "")
    out = out.replace(p_negative, "->")
    out = out.replace(p_green, "<>")
    out = out.replace(p_yellow, "! >")
    out = out.replace(p_red, "!!!!>>>>")
    return out

_COLOR_LOOKUP_TABLE = {
    "red":p_red,
    "green":p_green,
    "yellow":p_yellow,
    "turquoise":p_turquoise,
    "pink":p_pink,
    "light_green":p_light_green,
    "gray":p_gray,
    "gold":p_gold,
    "light_blue":p_light_blue,
    "negative":p_negative,
}

def remove_escape_sequences(string:str) -> str:
    for seq in _COLOR_LOOKUP_TABLE.values():
        string = string.replace(seq, "")
    string = string.replace(p_reset, "")
    return string


class TextColouring:
    @staticmethod
    def red(text:str) -> str:
        """
        :return: Returns the text with ANSII escape sequences at the beginning and end.
        """
        return f"{p_red}{text}{p_reset}"


    @staticmethod
    def green(text:str) -> str:
        """
        :return: Returns the text with ANSII escape sequences at the beginning and end.
        """
        return f"{p_green}{text}{p_reset}"


    @staticmethod
    def negative(text:str) -> str:
        """
        :return: Returns the text with ANSII escape sequences at the beginning and end.
        """
        return f"{p_negative}{text}{p_reset}"


    @staticmethod
    def yellow(text:str) -> str:
        """
        :return: Returns the text with ANSII escape sequences at the beginning and end.
        """
        return f"{p_yellow}{text}{p_reset}"


    @staticmethod
    def colour(text:str, colour:str) -> str:
        """
        Returns the text with corresponding ANSII escape sequences.
        Currently supported colours are:
        red, green, yellow, turquoise, pink, light_green, gray, gold, light_blue, negative
        :param text: The text to colour
        :param colour: The colour it should have.
        """
        if colour.lower() in _COLOR_LOOKUP_TABLE:
            return f"{_COLOR_LOOKUP_TABLE[colour.lower()]}{text}{p_reset}"
        return text