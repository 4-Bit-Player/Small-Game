
class TemporaryDisablePrintUpdates:
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def n_print(*values: object, sep: str = " "):
    print(*values, sep=sep, end="")

def toggle_ansi():
    pass

def n_exit():
    pass

p_red:str = "!!!!>>>>"
p_yellow:str = "!  >"
p_green:str = "<>"
p_reset:str = ""
p_negative:str = "->"

