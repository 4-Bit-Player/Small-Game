from enum import Enum

class SpecialChar(Enum):
    ArrowUp       = 0
    ArrowDown     = 1
    ArrowLeft     = 2
    ArrowRight    = 3
    F1            = 4
    F2            = 5
    F3            = 6
    F4            = 7
    F5            = 8
    F6            = 9
    F7            = 10
    F8            = 11
    F9            = 12
    F10           = 13
    F11           = 14
    F12           = 15
    Backspace     = 16
    Pos1          = 17
    End           = 18
    Escape        = 19
    PageUp        = 20
    PageDown      = 21
    Insert        = 22
    Delete        = 23
    InvalidKey    = 24
    NotSpecialKey = 25
    KeyboardInterrupt = 26


class Key:
    def __init__(self, val:str="",
                 is_special_char:bool=False,
                 pressed_special_char:SpecialChar=SpecialChar.NotSpecialKey,
                 ctrl_pressed:bool=False,
                 alt_pressed:bool = False,
                 shift_pressed:bool=False,
                 is_final:bool = False
                 ):
        self.val:str=val
        self.is_special_char:bool=is_special_char
        self.pressed_special_key:SpecialChar=pressed_special_char
        self.ctrl_pressed:bool=ctrl_pressed
        self.alt_pressed:bool=alt_pressed
        self.shift_pressed:bool=shift_pressed
        if is_final:
            self.__hash = (f"Key{self.val}{self.pressed_special_key.value}{self.ctrl_pressed}{self.shift_pressed}"
                           f"{self.alt_pressed}")
        else:
            self.__hash = ""
        self.__is_final = is_final

    def copy(self) -> 'Key':
        return  Key(val=self.val, is_special_char=self.is_special_char, pressed_special_char=self.pressed_special_key,
                 ctrl_pressed=self.ctrl_pressed, alt_pressed=self.alt_pressed, shift_pressed=self.shift_pressed,
                 is_final=self.__is_final)

    def _finalize_class(self) -> 'Key':
        """Sets itself to read only and returns itself."""
        self.__hash = self.__hash__()
        self.__is_final = True
        return self

    def class_is_read_only(self) -> bool:
        return self.__is_final

    def __str__(self) -> str:
        return (f"Key: Val:{self.val}, Special: {self.pressed_special_key.name}, IsSpecial:{self.is_special_char}, "
                f"Shift:{self.shift_pressed}, Ctrl:{self.ctrl_pressed}, Alt:{self.alt_pressed}, Read only:{self.__is_final}")

    def __copy__(self):
        return Key(val=self.val, is_special_char=self.is_special_char, pressed_special_char=self.pressed_special_key,
                 ctrl_pressed=self.ctrl_pressed, alt_pressed=self.alt_pressed, shift_pressed=self.shift_pressed,
                 is_final=self.__is_final)

    def __eq__(self, other):
        if isinstance(other, Key):
            if self.is_special_char:
                return (self.pressed_special_key == other.pressed_special_key
                        and self.shift_pressed == other.shift_pressed
                        and self.alt_pressed == other.alt_pressed
                        and self.ctrl_pressed == other.ctrl_pressed)
            return self.val == other.val
        if isinstance(other, SpecialChar):
            return self.is_special_char and self.pressed_special_key == other
        if isinstance(other, str):
            return self.is_special_char and self.val == other

        raise ValueError(f"Only Key, SpecialChar and strings are supported, not {type(other)}.")

    def __hash__(self):
        if self.__is_final:
            return self.__hash
        return (f"Key{self.val}{self.pressed_special_key.value}{self.ctrl_pressed}{self.shift_pressed}"
                f"{self.alt_pressed}")

    def __setattr__(self, key, value):
        if f"_{self.__class__.__name__}__is_final" in self.__dict__ and self.__is_final:
            raise ValueError("!!! This Class Is Read Only !!!")
        self.__dict__[key] = value


