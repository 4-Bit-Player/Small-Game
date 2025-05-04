from typing import Deque
from decoration import colors
from decoration.deco import line_r


class TempInput:
    def __init__(self, val:str=""):
        if val == "":
            self._temp_input:list[str] = []
            self._size:int = 0
        else:
            self._temp_input:list[str] = [x for x in val]
            self._size:int = len(self._temp_input)

    def __iadd__(self, other:str):
        self._temp_input.append(other)
        self._size += 1
        return self

    def __add__(self, other):
        return self._temp_input[:] + [other]


    def __len__(self):
        return len(self._temp_input)

    def rm_last_char(self):
        if len(self._temp_input) == 0:
            return
        self._size -= 1
        self._temp_input.pop()

    def text(self):
        return "".join(self._temp_input)

    def clear(self):
        self._size = 0
        self._temp_input.clear()

    @property
    def size(self):
        return self._size







class KeyinputIndexClass:
    def __init__(self, index:int, limit:int, persistent:bool):
        self._index:int = index
        self._limit:int = limit
        self._persistent:bool = persistent
        self._temp_input:TempInput = TempInput()
        self.invalid:bool = False

    @property
    def index(self):
        return self._index


    @index.setter
    def index(self, val:int):
        if val > self._limit:
            self._index = 1
            return
        elif val < 0:
            self._index = self._limit
            return
        self._index = val

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, val:int):
        if self._index > val:
            self._index = val
        self._limit = val

    @property
    def temp_input(self):
        return self._temp_input

    @temp_input.setter
    def temp_input(self, val:TempInput):
        if not isinstance(val, TempInput):
            raise ValueError(f"Trying to set wrong value type as temp input: {type(val)}")
        self._temp_input = val






class LAClass:
    def __init__(self, current_location:dict[str:any]):
        self.index = KeyinputIndexClass(1,1,True)
        self.active = True
        self._events:Deque[str] = Deque(["" for _ in range(5)])
        self.location = current_location
        self.updated = True
        self.paused = False
        self.combat_init = False
        self.combat = False



    def get_text(self, header:str=""):
        l_r = line_r()
        out:list[list|str] = [
            self.index, [
                header + "\n" + l_r +
                f'\nYou are wandering through the {self.location["name"]} looking for usable Items...\n' + l_r
            ],
            list(self._events), [l_r],
            [f"{colors.red}Invalid number, please pick a number from 1 to {self.index.limit}{colors.reset}" if self.index.invalid else ""],
            ["Action: " + self.index.temp_input.text() if self.index.temp_input.text() else ""],


        ]


        #if self.out:
        #    out.append([self.out])
        if self.combat_init:
            out.append("Run away!")
        elif not self.combat:
            out.append("Stop searching.")
        else:
            out.append("Fight!")

        return return_screen_prt_h(out)

    @property
    def events(self):
        return self._events.copy()

    def add_event(self, event:str):
        self.updated = True
        if len(self._events) > 4:
            self._events.pop()
        self._events.appendleft(event)




def return_screen_prt_h(lists, start=1):
    num = start
    selected = 0
    lines:list[str] = []
    if isinstance(lists[0], KeyinputIndexClass):
        selected = lists[0].index
    for line in lists:

        if isinstance(line, list):
            if len(line) == 0:
                lines.append("")
                continue
            if line[0] == 1:
                for l in line[1:]:
                    if num == selected:
                        l_line = colors.negative + str(num) + ". " + str(l) + " " + colors.reset
                    else:
                        l_line = (str(num) + ". " + str(l))
                    num += 1
                    lines.append(l_line)
            else:
                for l in line:
                    lines.append(l)

        if isinstance(line, str):
            if num == selected:
                l_line = colors.negative + str(num) + ". " + str(line) + " " + colors.reset
            else:
                l_line = (str(num) + ". " + str(line))
            num += 1
            lines.append(l_line)
    if len(lines) == 0:
        return ""
    return "\n".join(lines)





















