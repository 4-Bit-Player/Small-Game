from ._print_queue import get_print_queue, set_print_queue
from ._printclass import PrintClass
from threading import Thread
from queue import Queue

_started:bool = False
_print_thread: None|Thread = None

def _exec_print_thread(print_q: Queue, terminal_reset_allowed:bool):
    test = PrintClass(print_q, terminal_reset_allowed)
    test.run()




def init_print(print_q:Queue|None = None, terminal_reset_allowed:bool=True) -> Thread:
    """
    Initializes the print thread.
    If not called the n_print function will not work.

    :param print_q: The queue it should use for communication. Creates its own by default.
    :param terminal_reset_allowed: If the library is allowed to fully reset the terminal.
    :return: Returns the thread running the print class.
    """
    global _started, _print_thread
    if _started:
        return _print_thread
    _started = True
    if print_q is not None:
        set_print_queue(print_q)
        return _print_thread
    p_queue = get_print_queue()
    _print_thread = Thread(target=_exec_print_thread, args=[p_queue, terminal_reset_allowed], daemon=True)
    _print_thread.start()
    return _print_thread



