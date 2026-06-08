import sys
from threading import Thread
from time import perf_counter, sleep
try:
    from printing import TemporaryDisablePrintUpdates
except ImportError:
    from ._fallback_printing import TemporaryDisablePrintUpdates


if "win" in sys.platform:
    from ._win_console_input import thread_func
else:
    from ._linux_console_input import thread_func
from ._Key import Key, SpecialChar
from ._Buffer import Buffer


_input_thread:Thread = Thread()
_communication_lst:list[int] = [1]
_key_kju:Buffer[Key] = Buffer(100)

def init_keyboard_input():
    """
    Initializes and starts the input threads.
    """
    global _input_thread
    if not _input_thread.is_alive():
        _input_thread = Thread(target=thread_func, args=[_key_kju, _communication_lst], daemon=True)
        _input_thread.start()
    _keyboard_input_paused = False
    _keyboard_input_stop = False
    _communication_lst[0] = 1


def stop_keyboard_input():
    """
    Stopps the input thread.
    It has to get initialized again to restart.
    """
    _communication_lst[0] = -1
    _input_thread.join()


def pause_keyboard_input():
    """
    Pauses the keyboard input.
    You can resume it whenever.
    If there are inputs left in the stdin when it resumes it will read them.
    """
    _communication_lst[0] = 0


def resume_keyboard_input():
    """
    Resumes the key input threads.
    Does not start the thread if it got stopped, only when paused.
    """
    _communication_lst[0] = 1


_null_key = Key("", is_final=True)
def get_key(blocking:bool=True, remove_cached_chars:bool = False) -> Key:
    """
    Remember checking for KeyboardInterrupt. :)
    Obviously it can't be non-blocking and removing the cached chars at the same time.
    If it is set to non-blocking and removing the chars, non-blocking will count.
    :param remove_cached_chars: If it should remove all pressed keys in the queue.
    :param blocking: If it should wait until it gets a key.
    :return: A Key
    """
    if not blocking:
        if _key_kju.size() > 0:
            return _key_kju.pop_left()
        if not _input_thread.is_alive():
            raise KeyboardInterrupt("Either the input thread wasn't initialized, or it got interrupted/stopped!")
        return _null_key

    if remove_cached_chars:
        for key in _key_kju:
            if key.is_special_char and key.pressed_special_key == SpecialChar.KeyboardInterrupt:
                raise KeyboardInterrupt()
        _key_kju.clear()

    if not _input_thread.is_alive():
        raise KeyboardInterrupt("Either the input thread wasn't initialized, or it got interrupted/stopped!")
    while len(_key_kju) <= 0:
        sleep(0.05)
    return _key_kju.pop_left()


_orig_input = input
def build_in_input(__prompt: object = "") -> str:
    """
    Read a string from standard input.  The trailing newline is stripped.

    The prompt string, if given, is printed to standard output without a
    trailing newline before reading input.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), raise EOFError.
    On *nix systems, readline is used if available.


    (pauses the input thread for the call and resumes it afterward.)
    """
    pause_keyboard_input()
    with TemporaryDisablePrintUpdates():
        out = _orig_input(__prompt)
    resume_keyboard_input()
    return out