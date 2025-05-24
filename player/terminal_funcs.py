import sys
from time import sleep, perf_counter
from threading import Thread, Lock
from tools.LList import LinkedList

if sys.platform == "win32":
    from msvcrt import getch as _getch
else:
    import readchar
    _char_buffer = b''
    _arrow_keys = [ b'\x1b[B',b'\x1b[A', b'\x1b[C', b'\x1b[D']
    _f_keys = {b'\x1b0P', b'\x1b0Q', b'\x1b0R', b'\x1b0S', b'\x1b[15~', b'\x1b[17~', b'\x1b[18~', b'\x1b[19~', b'\x1b[20~', b'\x1b[21~'}
    _char_lookup = {
        b'\n': b'\r',
        b'\x1b[B': b'P',      # arrow down
        b'\x1b[A': b'H',      # Up arrow key
        b'\x1b[C': b'M',      # Right arrow key
        b'\x1b[D': b'K',      # Left arrow key
        b'\xc2\xa7': b'\xf5', # shift+3 german layout
        b'\x1b\x1b': b'\x1b', # escape key
        b'\x7f': b'\x08',     # backspace
        b'\x08': b'\x7f',     # Ctrl + Backspace
        b'\x1b0P': b';',      # F1
        b'\x1b0Q': b'<',      # F2
        b'\x1b0R': b'=',      # F3
        b'\x1b0S': b'>',      # F4
        b'\x1b[15~': b'?',    # F5
        b'\x1b[17~': b'@',    # F6
        b'\x1b[18~': b'A',    # F7
        b'\x1b[19~': b'B',    # F8
        b'\x1b[20~': b'C',    # F9
        b'\x1b[21~': b'D',    # F10

    }
    def _getch():
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

_input_thread = Thread
_key_cache:LinkedList = LinkedList()
_lock = Lock()





def get_char(remove_cached_input=True):
    if not remove_cached_input:
        while len(_key_cache) == 0:
            with _lock:
                continue
        return _key_cache.popleft()
    #return input_funcs.readkey()
    old_time= perf_counter()
    while True:
        if len(_key_cache) == 0:
            with _lock:
                continue
        key = _key_cache.popleft()
        new_time = perf_counter()
        if new_time - old_time < 0.01:
            continue
        break
    return key


def init_keyboard_input() -> None:
    global _input_thread

    _input_thread = Thread(target=_thread_func, daemon=True)
    _input_thread.start()


def _thread_func():
    global _key_cache
    while True:
        with _lock:
            key = _getch()
            #while len(_key_cache) > 100:
            #    _key_cache.popleft()
            _key_cache.append(key)
        sleep(0.01)

"""
def readchar() -> str:
    \"""Reads a single character from the input stream.
    Blocks until a character is available.\"""

    return sys.stdin.read(1).encode()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)
    try:
        term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
        termios.tcsetattr(fd, termios.TCSAFLUSH, term)

        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readkey() -> str:
    \"""Get a keypress. If an escaped key is pressed, the full sequence is
    read and returned as noted in `_posix_key.py`.\"""

    c1 = readchar()
    print(c1)
    sleep(1)

    if c1 != "\x1B":
        return c1

    c2 = readchar()
    if c2 not in "\x4F\x5B":
        return c1 + c2

    c3 = readchar()
    if c3 not in "\x31\x32\x33\x35\x36":
        return c1 + c2 + c3

    c4 = readchar()
    if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
        return c1 + c2 + c3 + c4

    c5 = readchar()
    return c1 + c2 + c3 + c4 + c5

"""