import queue
from player import user


_print_queue = queue.Queue()
_show_fps = False
_constant_refresh = False


def n_print(*args):
    _print_queue.put([args, user.settings["centered_screen"]])

def toggle_fps():
    global _show_fps
    _show_fps = not _show_fps
    _print_queue.put(["show fps", _show_fps])

def toggle_constant_refresh():
    global _constant_refresh
    _constant_refresh = not _constant_refresh
    _print_queue.put(["constant refresh", _constant_refresh])

def change_fps_limit(new_fps):
    _print_queue.put(["change fps", new_fps])