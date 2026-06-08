import msvcrt
from time import sleep
from threading import Thread
from ._Buffer import Buffer
from ._Key import Key, SpecialChar


_lookup_table = {
    "\r":Key("\n", is_final=True),
    "\n":Key("\n", ctrl_pressed=True, is_final=True),
    "\x08":Key("\x08", is_special_char=True, pressed_special_char=SpecialChar.Backspace, is_final=True),
    "\x7f":Key("\x08", is_special_char=True, pressed_special_char=SpecialChar.Backspace, ctrl_pressed=True, is_final=True),
    ";":Key(is_special_char=True,pressed_special_char=SpecialChar.F1, is_final=True),
    "T":Key(is_special_char=True,pressed_special_char=SpecialChar.F1, shift_pressed=True, is_final=True),
    "^":Key(is_special_char=True,pressed_special_char=SpecialChar.F1, ctrl_pressed=True, is_final=True),
    "h":Key(is_special_char=True,pressed_special_char=SpecialChar.F1, alt_pressed=True, is_final=True),
    "<":Key(is_special_char=True,pressed_special_char=SpecialChar.F2, is_final=True),
    "U":Key(is_special_char=True,pressed_special_char=SpecialChar.F2, shift_pressed=True, is_final=True),
    "_":Key(is_special_char=True,pressed_special_char=SpecialChar.F2, ctrl_pressed=True, is_final=True),
    "i":Key(is_special_char=True,pressed_special_char=SpecialChar.F2, alt_pressed=True, is_final=True),
    "=":Key(is_special_char=True,pressed_special_char=SpecialChar.F3, is_final=True),
    "V":Key(is_special_char=True,pressed_special_char=SpecialChar.F3, shift_pressed=True, is_final=True),
    "`":Key(is_special_char=True,pressed_special_char=SpecialChar.F3, ctrl_pressed=True, is_final=True),
    "j":Key(is_special_char=True,pressed_special_char=SpecialChar.F3, alt_pressed=True, is_final=True),
    ">":Key(is_special_char=True,pressed_special_char=SpecialChar.F4, is_final=True),
    "W":Key(is_special_char=True,pressed_special_char=SpecialChar.F4, shift_pressed=True, is_final=True),
    "a":Key(is_special_char=True,pressed_special_char=SpecialChar.F4, ctrl_pressed=True, is_final=True),
    "k":Key(is_special_char=True,pressed_special_char=SpecialChar.F4, alt_pressed=True, is_final=True),
    "?":Key(is_special_char=True,pressed_special_char=SpecialChar.F5, is_final=True),
    "X":Key(is_special_char=True,pressed_special_char=SpecialChar.F5, shift_pressed=True, is_final=True),
    "b":Key(is_special_char=True,pressed_special_char=SpecialChar.F5, ctrl_pressed=True, is_final=True),
    "l":Key(is_special_char=True,pressed_special_char=SpecialChar.F5, alt_pressed=True, is_final=True),
    "@":Key(is_special_char=True,pressed_special_char=SpecialChar.F6, is_final=True),
    "Y":Key(is_special_char=True,pressed_special_char=SpecialChar.F6, shift_pressed=True, is_final=True),
    "c":Key(is_special_char=True,pressed_special_char=SpecialChar.F6, ctrl_pressed=True, is_final=True),
    "m":Key(is_special_char=True,pressed_special_char=SpecialChar.F6, alt_pressed=True, is_final=True),
    "A":Key(is_special_char=True,pressed_special_char=SpecialChar.F7, is_final=True),
    "Z":Key(is_special_char=True,pressed_special_char=SpecialChar.F7, shift_pressed=True, is_final=True),
    "d":Key(is_special_char=True,pressed_special_char=SpecialChar.F7, ctrl_pressed=True, is_final=True),
    "n":Key(is_special_char=True,pressed_special_char=SpecialChar.F7, alt_pressed=True, is_final=True),
    "B":Key(is_special_char=True,pressed_special_char=SpecialChar.F8, is_final=True),
    "[":Key(is_special_char=True,pressed_special_char=SpecialChar.F8, shift_pressed=True, is_final=True),
    "e":Key(is_special_char=True,pressed_special_char=SpecialChar.F8, ctrl_pressed=True, is_final=True),
    "o":Key(is_special_char=True,pressed_special_char=SpecialChar.F8, alt_pressed=True, is_final=True),
    "C":Key(is_special_char=True,pressed_special_char=SpecialChar.F9, is_final=True),
    "\\":Key(is_special_char=True,pressed_special_char=SpecialChar.F9, shift_pressed=True, is_final=True),
    "f":Key(is_special_char=True,pressed_special_char=SpecialChar.F9, ctrl_pressed=True, is_final=True),
    "p":Key(is_special_char=True,pressed_special_char=SpecialChar.F9, alt_pressed=True, is_final=True),
    "D":Key(is_special_char=True,pressed_special_char=SpecialChar.F10, is_final=True),
    "]":Key(is_special_char=True,pressed_special_char=SpecialChar.F10, shift_pressed=True, is_final=True),
    "g":Key(is_special_char=True,pressed_special_char=SpecialChar.F10, ctrl_pressed=True, is_final=True),
    "q":Key(is_special_char=True,pressed_special_char=SpecialChar.F10, alt_pressed=True, is_final=True),
    "E":Key(is_special_char=True,pressed_special_char=SpecialChar.F11, is_final=True),
    b"\xc2\x87".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.F11, shift_pressed=True, is_final=True),
    b"\xc2\x89".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.F11, ctrl_pressed=True, is_final=True),
    b"\xc2\x8b".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.F11, alt_pressed=True, is_final=True),
    "F":Key(is_special_char=True,pressed_special_char=SpecialChar.F12, is_final=True),
    b"\xc2\x88".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.F12, shift_pressed=True, is_final=True),
    b"\xc2\x8a".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.F12, ctrl_pressed=True, is_final=True),
    b"\xc2\x8c".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.F12, alt_pressed=True, is_final=True),
    "R":Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, is_final=True),
    #"\xc2\x91":Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, shift_pressed=True, is_final=True),
    b"\xc2\x92".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, ctrl_pressed=True, is_final=True),
    b"\xc2\xa2".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, alt_pressed=True, is_final=True),
    "S":Key(is_special_char=True,pressed_special_char=SpecialChar.Delete, is_final=True),
    #"\xc2\x91":Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, shift_pressed=True, is_final=True),
    b"\xc2\x93".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, ctrl_pressed=True, is_final=True),
    b"\xc2\xa3".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, alt_pressed=True, is_final=True),
    "G":Key(is_special_char=True,pressed_special_char=SpecialChar.Pos1, is_final=True),
    #"\xc2\x91":Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, shift_pressed=True, is_final=True),
    "w":Key(is_special_char=True,pressed_special_char=SpecialChar.Pos1, ctrl_pressed=True, is_final=True),
    b"\xc2\x97".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.Pos1, alt_pressed=True, is_final=True),
    "O":Key(is_special_char=True,pressed_special_char=SpecialChar.End, is_final=True),
    #"G":Key(is_special_char=True,pressed_special_char=SpecialChar.Insert, shift_pressed=True, is_final=True),
    "u":Key(is_special_char=True,pressed_special_char=SpecialChar.End, ctrl_pressed=True, is_final=True),
    b"\xc2\x9f".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.End, alt_pressed=True, is_final=True),
    "I":Key(is_special_char=True,pressed_special_char=SpecialChar.PageUp, is_final=True),
    b"\xc2\x86".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.PageUp, ctrl_pressed=True, is_final=True),
    b"\xc2\x99".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.PageUp, alt_pressed=True, is_final=True),
    "Q":Key(is_special_char=True,pressed_special_char=SpecialChar.PageUp, is_final=True),
    "v":Key(is_special_char=True,pressed_special_char=SpecialChar.PageUp, ctrl_pressed=True, is_final=True),
    b"\xc2\xa1".decode(encoding="utf-8"):Key(is_special_char=True,pressed_special_char=SpecialChar.PageUp, alt_pressed=True, is_final=True),
    "H":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowUp, is_final=True),
    b"\xc2\x8d".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowUp, ctrl_pressed=True, is_final=True),
    b"\xc2\x98".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowUp, alt_pressed=True, is_final=True),
    "M":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowRight, is_final=True),
    b"t".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowRight, ctrl_pressed=True, is_final=True),
    b"\xc2\x9d".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowRight, alt_pressed=True, is_final=True),
    "P":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowDown, is_final=True),
    b"\xc2\x91".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowDown, ctrl_pressed=True, is_final=True),
    b"\xc2\xa0".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowDown, alt_pressed=True, is_final=True),
    "K":Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowLeft, is_final=True),
    b"s".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowLeft, ctrl_pressed=True, is_final=True),
    b"\xc2\x9b".decode(encoding="utf-8"):Key(is_special_char=True, pressed_special_char=SpecialChar.ArrowLeft, alt_pressed=True, is_final=True),

}

def _read(input_kju:list[str], should_run:list[bool]):
    while should_run:
        if not should_run[0]:
            sleep(0.1)
            continue
        char = msvcrt.getwch()
        #print(char, char.encode())
        input_kju.append(char)

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


def thread_func(kju:Buffer[Key], communication_lst:list[int]) -> None:
    input_kju:Buffer[str] = Buffer(100)
    thread_should_run = [True]
    sub_thread = Thread(target=_read, args=[input_kju, thread_should_run], daemon=True)
    sub_thread.start()
    sleep_time = 0
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
                sleep_time += 0.001
            sleep(sleep_time)
            continue
        sleep_time = 0
        first_char = input_kju.pop_left()
        if first_char == "\x03":
            thread_should_run.pop()
            kju.append(Key(is_special_char=True, pressed_special_char=SpecialChar.KeyboardInterrupt, is_final=True))
            return None
        elif first_char == "\x1b":
            kju.append(Key(is_special_char=True, pressed_special_char=SpecialChar.Escape, is_final=True))
            continue
        elif first_char == "\x00":
            _wait_for_input(input_kju)
            second_char = input_kju.pop_left()
            if second_char in _lookup_table:
                kju.append(_lookup_table[second_char])
                continue
        elif first_char == "à":
            if _has_char(input_kju):
                second_char = input_kju.pop_left()
                if second_char in _lookup_table:
                    kju.append(_lookup_table[second_char])
                    continue
        elif first_char in "\r\n\x08\x7f":
            kju.append(_lookup_table[first_char])
            continue
        kju.append(Key(first_char, is_final=True))

