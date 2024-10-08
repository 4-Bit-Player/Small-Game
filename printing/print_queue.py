import queue
from player import user


print_queue = queue.Queue()
show_fps = False
constant_refresh = False


def n_print(*args):
    print_queue.put([args, user.settings["centered_screen"]])

def toggle_fps():
    global show_fps
    show_fps = not show_fps
    print_queue.put(["show fps", show_fps])

def toggle_constant_refresh():
    global constant_refresh
    constant_refresh = not constant_refresh
    print_queue.put(["constant refresh", constant_refresh])