import queue
from player import user
print_queue = queue.Queue()


def n_print(*args):
    print_queue.put([args, user.settings["centered_screen"]])

def toggle_fps():
    print_queue.put(["toggle fps"])

def toggle_constant_refresh():
    print_queue.put(["toggle constant refresh"])