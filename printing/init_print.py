from player import user
from printing import print_queue, printclass
import threading
from queue import Queue


_started = False


def _exec_print_thread(print_q: Queue):
    test = printclass.PrintClass(print_q, user.test)
    test.run()




def init_print():
    global _started
    if _started:
        return
    _started = True

    print_thread = threading.Thread(target=_exec_print_thread, args=[print_queue._print_queue], daemon=True)
    print_thread.start()



