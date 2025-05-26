from queue import Queue
from player import user


_print_queue = Queue()
_show_fps = False
_constant_refresh = False


def n_print(text:str):
    _print_queue.put([text, user.settings["centered_screen"]])

def toggle_fps():
    global _show_fps
    _show_fps = not _show_fps
    _print_queue.put([("show fps",), _show_fps])

def toggle_constant_refresh():
    global _constant_refresh
    _constant_refresh = not _constant_refresh
    _print_queue.put([("constant refresh",), _constant_refresh])

def change_fps_limit(new_fps):
    _print_queue.put([("change fps",), new_fps])


class TemporaryDisablePrintUpdates:
    def __enter__(self):
        self.fps_state = _show_fps
        self.constant_refresh_state = _constant_refresh

        if _show_fps:
            toggle_fps()
        if _constant_refresh:
            toggle_constant_refresh()

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.fps_state and not _show_fps:
            toggle_fps()

        if self.constant_refresh_state and not _constant_refresh:
            toggle_constant_refresh()

        if exc_tb is None and exc_val is None and exc_tb is None:
            return True
        return False