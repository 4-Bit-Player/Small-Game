from ._InputClass import KeyInputIndexClass, TempInput

class NonBlockTempInput(TempInput):
    def __init__(self, parent_class):
        super().__init__()
        self._parent_class:NonBlockIndexClass = parent_class

    def __iadd__(self, other:str|list[str]|TempInput):
        self._parent_class._got_updated()
        return super().__iadd__(other)


    def rm_last_char(self):
        self._parent_class._got_updated()
        return super().rm_last_char()


    def clear(self):
        self._parent_class._got_updated()
        return super().clear()




class NonBlockIndexClass(KeyInputIndexClass):
    def __init__(self, index:int=1, limit:int=1):
        super().__init__(index, limit)
        self._updates = True
        self._temp_input = NonBlockTempInput(self)

    @property
    def updates(self) -> bool:
        if self._updates:
            self._updates = False
            return True
        return False

    def _got_updated(self):
        self._updates = True






