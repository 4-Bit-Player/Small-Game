
class TempInput:
    """
    Class for saving the state of the user input
    """
    def __init__(self, val:list=None):
        if val is None:
            self._temp_input:list[str] = []
            self._size:int = 0
        else:
            self._temp_input:list[str] = val
            self._size:int = len(self._temp_input)

    def rm_last_char(self):
        """
        Removes the last character from its list.
        :return: Returns nothing
        """
        if len(self._temp_input) == 0:
            return
        self._size -= 1
        self._temp_input.pop()


    def text(self):
        """
        Returns a copy of the content of itself as a string.
        :return: A string
        """
        return "".join(self._temp_input)

    def clear(self):
        """
        Clears its list.
        :return: Nothing
        """
        self._size = 0
        self._temp_input.clear()

    @property
    def size(self):
        """
        :return: The size of its list
        """
        return self._size

    @property
    def input_list(self)->list[str]:
        """
        :return: A copy of the internal list of chars.
        """
        return self._temp_input[:]

    def __iadd__(self, other:'str|list[str]|TempInput'):
        if isinstance(other, str):
            self._temp_input.append(other)
            self._size += 1

        elif isinstance(other, list):
            for thing in other:
                if isinstance(thing, str):
                    continue
                raise ValueError(f"Trying to add the wrong type to a TempInput instance using a list.\nThe list has to contain only strings, not {type(thing)}.")
            self._temp_input += other[:]
            self._size += len(other)

        elif isinstance(other, TempInput):
            self._temp_input += other.input_list
            self._size += other.size
        return self

    def __add__(self, other:'str|list[str]|TempInput') -> 'TempInput':
        if isinstance(other, str):
            return TempInput(self._temp_input[:] + [other])

        if isinstance(other, list):
            return TempInput(self._temp_input[:] + other)

        if not isinstance(other, TempInput):
            raise NotImplementedError(f"No implementation for adding with Type '{type(other)}'")

        return TempInput(self._temp_input[:]+other.input_list)

    def __len__(self):
        return len(self._temp_input)

    def __repr__(self):
        return f"TempInput; size: {self._size}; chars: {self._temp_input}"

    def __str__(self):
        return "".join(self._temp_input)

    def __bool__(self) -> bool:
        return len(self._temp_input) != 0



class KeyInputIndexClass:
    def __init__(self, index:int=1, limit:int=1, persistent:bool=True):
        self._index:int = index
        self._limit:int = limit
        self._persistent:bool = persistent
        self._temp_input:TempInput = TempInput()
        self.invalid:bool = False

    @property
    def index(self) -> int:
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
    def limit(self) -> int:
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
        if not issubclass(type(val), TempInput):
            raise ValueError(f"Trying to set wrong value type as temp input: {type(val)}")
        self._temp_input = val


