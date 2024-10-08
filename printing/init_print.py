from player import user
from printing import print_queue, printclass
import threading
import queue


started = False


def _exec_print_thread(print_q: queue.Queue):
    test = printclass.PrintClass(print_q, user.test)
    test.start()




def init_print():
    global started
    if started:
        return
    started = True

    print_thread = threading.Thread(target=_exec_print_thread, args=[print_queue.print_queue], daemon=True)
    print_thread.start()



