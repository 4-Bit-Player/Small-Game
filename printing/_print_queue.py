from queue import Queue
from shutil import get_terminal_size

_print_queue = Queue()
_show_fps = False
_constant_refresh = False


def n_print(*values: object, sep: str = " ") -> None:
    """
    Function to display text to sys.stdout. :)

    :param sep: The seperator between values
    """
    _print_queue.put([sep.join([str(x) for x in values])])


def _send_arg_to_thread(arg, state):
    _print_queue.put([(arg,), state])


def n_exit() -> None:
    """
    Stops the print thread.
    """
    _send_arg_to_thread("exit", True)


def toggle_fps() -> None:
    """
    Toggles the visibility of the time it takes to display stuff.

    Unnecessary, and should not get used.
    """
    global _show_fps
    _show_fps = not _show_fps
    _send_arg_to_thread("show fps", _show_fps)



def toggle_constant_refresh() -> None:
    """
    Unnecessary debug function.

    It will recalculate and print the output every tick.

    Don't use it.
    """
    global _constant_refresh
    _constant_refresh = not _constant_refresh
    _send_arg_to_thread("constant refresh", _constant_refresh)


def change_fps_limit(new_fps: int) -> None:
    """
    Function to change the target amount of checks for new print data per second.

    :param new_fps: Amount of times per second it should check for new print data.
    """
    _send_arg_to_thread("change fps", new_fps)


def get_print_queue()->Queue:
    return _print_queue


def set_print_queue(q:Queue)->None:
    global _print_queue
    _print_queue = q


class TemporaryDisablePrintUpdates:
    """
    A class to pause the print updates.

    Usage:

    with TemporaryDisablePrintUpdates():
        print("Stuff you want to display.")

    Or:

    TemporaryDisablePrintUpdates.pause_print_updates()
    print("Stuff you want to display.")
    TemporaryDisablePrintUpdates.resume_print_updates()
    """
    def __enter__(self) -> None:
        self.pause_print_updates()
        self._fps_state = _show_fps
        self._constant_refresh_state = _constant_refresh


        #if _show_fps:
        #    toggle_fps()
        #if _constant_refresh:
        #    toggle_constant_refresh()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.resume_print_updates()

        if self._fps_state and not _show_fps:
            toggle_fps()

        if self._constant_refresh_state and not _constant_refresh:
            toggle_constant_refresh()

        if exc_tb is None and exc_val is None and exc_tb is None:
            return True
        return False

    @staticmethod
    def pause_print_updates() -> None:
        _send_arg_to_thread("pause", True)

    @staticmethod
    def resume_print_updates() -> None:
        _send_arg_to_thread("pause", False)


def get_terminal_width() -> int:
    return get_terminal_size()[0]



_centered_text:bool = False
def toggle_centered_text() -> None:
    """
    Toggles the centered state of the print thread.

    Centering is based on the set max line length, not on the actual line length.
    """
    global _centered_text
    _centered_text = not _centered_text
    _send_arg_to_thread("center text", _centered_text)


def center_text() -> None:
    """
    Tells the print thread to center the text based on the set line length.
    (Not based on the actual line length)

    It is recommended to set a max length for the text.
    """
    global _centered_text
    _centered_text = True
    _send_arg_to_thread("center text", _centered_text)


def uncenter_text() -> None:
    """
    Tells the print thread to not center the text.
    """
    global _centered_text
    _centered_text = False
    _send_arg_to_thread("center text", _centered_text)




