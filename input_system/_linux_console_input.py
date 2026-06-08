import sys
import termios
import tty
from threading import Thread
import atexit
from time import sleep
from ._Key import Key, SpecialChar
from ._Buffer import Buffer


__extra_key_table = {
    "2": Key(is_special_char=True, shift_pressed=True),
    "3": Key(is_special_char=True, alt_pressed=True),
    "4": Key(is_special_char=True, shift_pressed=True, alt_pressed=True),
    "5": Key(is_special_char=True, ctrl_pressed=True),
    "6": Key(is_special_char=True, ctrl_pressed=True, shift_pressed=True),
    "7": Key(is_special_char=True, ctrl_pressed=True, alt_pressed=True),
    "8": Key(is_special_char=True, ctrl_pressed=True, shift_pressed=True, alt_pressed=True),
}

def extra_key_check(kyu:Buffer[str]) -> Key:
    _wait_for_input(kyu)
    val = kyu.pop_left()
    if val in __extra_key_table:
        return __extra_key_table[val].copy()
    return Key(is_special_char=True, pressed_special_char=SpecialChar.InvalidKey, ctrl_pressed=False)

_f_key_lookup = {
    "P":Key(is_special_char=True, pressed_special_char=SpecialChar.F1, is_final=True),
    "Q":Key(is_special_char=True, pressed_special_char=SpecialChar.F2, is_final=True),
    "R":Key(is_special_char=True, pressed_special_char=SpecialChar.F3, is_final=True),
    "S":Key(is_special_char=True, pressed_special_char=SpecialChar.F4, is_final=True),
    "A":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowUp, is_final=True),
    "B":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowDown, is_final=True),
    "C":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowRight, is_final=True),
    "D":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowLeft, is_final=True),
    "H":Key(is_special_char=True, pressed_special_char=SpecialChar.Pos1, is_final=True),
    "F":Key(is_special_char=True, pressed_special_char=SpecialChar.End, is_final=True),
}

_double_char_lookup = {
    "2":Key(is_special_char=True, pressed_special_char=SpecialChar.Insert, is_final=True),
    "3":Key(is_special_char=True, pressed_special_char=SpecialChar.Delete, is_final=True),
    "5":Key(is_special_char=True, pressed_special_char=SpecialChar.PageUp, is_final=True),
    "6":Key(is_special_char=True, pressed_special_char=SpecialChar.PageDown, is_final=True),
    "15":Key(is_special_char=True, pressed_special_char=SpecialChar.F5, is_final=True),
    "17":Key(is_special_char=True, pressed_special_char=SpecialChar.F6, is_final=True),
    "18":Key(is_special_char=True, pressed_special_char=SpecialChar.F7, is_final=True),
    "19":Key(is_special_char=True, pressed_special_char=SpecialChar.F8, is_final=True),
    "20":Key(is_special_char=True, pressed_special_char=SpecialChar.F9, is_final=True),
    "21":Key(is_special_char=True, pressed_special_char=SpecialChar.F10, is_final=True),
    "23":Key(is_special_char=True, pressed_special_char=SpecialChar.F11, is_final=True),
    "24":Key(is_special_char=True, pressed_special_char=SpecialChar.F12, is_final=True),
}

_other_lookup_table = [
    Key(is_special_char=True, pressed_special_char=SpecialChar.Escape, is_final=True),
    Key(val="\x08",is_special_char=True, pressed_special_char=SpecialChar.Backspace, is_final=True),
    Key(val="\x08",is_special_char=True, ctrl_pressed=True, pressed_special_char=SpecialChar.Backspace, is_final=True),
]


def _read(input_kju:list[str], should_run:list[bool]):
    _init_terminal()
    try:
        while should_run:
            if not should_run[0]:
                sleep(0.1)
                continue
            char = sys.stdin.read(1)
            input_kju.append(char)
            #print(char.encode())
    finally:
        _restore_terminal()


def _has_char(kju:Buffer[str]) -> bool:
    if kju.size() > 0:
        return True
    sleep(0.0001)
    return kju.size() > 0


def _wait_for_input(kju:Buffer[str]):
    if len(kju) > 0:
        return
    while len(kju) <= 0:
        sleep(0.01)


def _restore_terminal():
    global _initialized
    if _initialized:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _old_terminal_settings)
        _initialized = False


def _init_terminal():
    global _initialized, _old_terminal_settings
    if _initialized:
        return
    fd = sys.stdin.fileno()
    _old_terminal_settings = termios.tcgetattr(fd)
    _initialized = True
    tty.setcbreak(fd)

_initialized = False
_old_terminal_settings = None
_invalid_key = Key(is_special_char=True, pressed_special_char=SpecialChar.InvalidKey, is_final=True)
def thread_func(kju:Buffer[Key], communication_lst:list[int]) -> None:
    atexit.register(_restore_terminal)
    input_kju: Buffer[str] = Buffer(100)
    thread_should_run = [True]
    sub_thread = Thread(target=_read, args=[input_kju, thread_should_run], daemon=True)
    sub_thread.start()
    sleep_time = 0
    try:
        while True:
            if communication_lst[0] != 1:
                thread_should_run[0] = False
                while communication_lst[0] != 1:
                    if communication_lst[0] == -1:
                        thread_should_run.pop()
                        #   sub_thread.join()
                        return None
                    sleep(0.1)
                thread_should_run[0] = True

            if not _has_char(input_kju):
                if sleep_time < 0.1:
                    sleep_time += 0.01
                sleep(sleep_time)
                continue
            sleep_time = 0

            first_char = input_kju.pop_left()
            if first_char == "\x1b":
                if not _has_char(input_kju):
                    kju.append(_other_lookup_table[0]) # Esc key :)
                    continue
                second_char = input_kju.pop_left()
                if second_char == "\x1b":
                    kju.append(Key(is_special_char=True, alt_pressed=True, pressed_special_char=SpecialChar.Escape, is_final=True))
                    continue
                if second_char == "O":
                    kju.append(_f_key_lookup[input_kju.pop_left()])
                    continue
                if second_char == "[":
                    third_char = input_kju.pop_left()
                    if third_char in _f_key_lookup:
                        kju.append(_f_key_lookup[third_char])
                        continue
                    fourth_char = input_kju.pop_left()

                    if third_char == "1":
                        if fourth_char == ";":
                            extra_key = extra_key_check(input_kju)
                            fifth_char = input_kju.pop_left()
                            if not fifth_char in _f_key_lookup:
                                kju.append(_invalid_key)
                                continue
                            extra_key.pressed_special_key = _f_key_lookup[fifth_char].pressed_special_key
                            extra_key._finalize_class()
                            kju.append(extra_key)
                            continue
                    if fourth_char == ";":
                        extra_key = extra_key_check(input_kju)
                        if input_kju.pop_left() != "~":
                            kju.append(_invalid_key)
                            continue
                        extra_key.pressed_special_key = _double_char_lookup[third_char].pressed_special_key
                        extra_key._finalize_class()
                        kju.append(extra_key)
                        continue
                    if fourth_char == "~":
                        kju.append(_double_char_lookup[third_char])
                        continue
                    fifth_char = input_kju.pop_left()
                    if fifth_char == "~":
                        kju.append(_double_char_lookup[third_char+fourth_char])
                        continue
                    if fifth_char != ";":
                        kju.append(_invalid_key)
                        continue
                    extra_key = extra_key_check(input_kju)
                    sixth_char = input_kju.pop_left()
                    if sixth_char != "~":
                        kju.append(_invalid_key)
                        continue
                    extra_key.pressed_special_key = _double_char_lookup[third_char+fourth_char].pressed_special_key
                    extra_key._finalize_class()
                    kju.append(extra_key)
                    continue
                first_char = second_char
            elif first_char in "\x08\x7f":
                if first_char == "\x08":
                    kju.append(_other_lookup_table[2])
                    continue
                kju.append(_other_lookup_table[1])
                continue
            kju.append(Key(first_char, is_final=True))

    except KeyboardInterrupt:
        kju.append(Key(is_special_char=True, pressed_special_char=SpecialChar.KeyboardInterrupt, is_final=True))
    finally:
        if communication_lst:
            communication_lst.pop()

