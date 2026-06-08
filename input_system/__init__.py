# V1.1
from ._key_input import key_input, wait_for_keypress, key_input_non_blocking, num_input, print_info_message
from ._text_input import text_input
from ._path_input import path_input
from ._InputClass import KeyInputIndexClass, TempInput
from ._terminal_funcs import init_keyboard_input, pause_keyboard_input, get_key, resume_keyboard_input, stop_keyboard_input
from ._NBInputClass import NonBlockIndexClass
from ._Key import Key, SpecialChar



from ._terminal_funcs import build_in_input as input
"""
    Intentionally hijacking the build in input function because the keypresses do get caught by the library if not handled correctly.
    It pauses the thread that checks for keypresses, calls the build in input function and resumes the thread afterwards.
"""
