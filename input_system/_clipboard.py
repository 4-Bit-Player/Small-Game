from sys import platform

from input_system import wait_for_keypress
try:
    from printing import n_print
except ImportError:
    from ._fallback_printing import n_print

if platform != "win32":
    import subprocess

    def get_clipboard():
        try:
            clipboard = subprocess.check_output(['xsel', '-b']).decode('utf-8').strip()
            return clipboard
        except FileNotFoundError:
            n_print("\nError: xsel command not found. Install it with 'sudo apt-get install xsel'\n(Press any key to continue)")
            wait_for_keypress()
            return ""
        except Exception as e:
            #print(f"Error reading clipboard: {e}")
            return ""

else:
    import ctypes

    CF_TEXT = 1
    kernel32 = ctypes.windll.kernel32
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32 = ctypes.windll.user32
    user32.GetClipboardData.restype = ctypes.c_void_p

    def get_clipboard() -> str:
        user32.OpenClipboard(0)
        try:
            if user32.IsClipboardFormatAvailable(CF_TEXT):
                data = user32.GetClipboardData(CF_TEXT)
                data_locked = kernel32.GlobalLock(data)
                text = ctypes.c_char_p(data_locked)
                value = text.value.decode("ansi")
                kernel32.GlobalUnlock(data_locked)
                return value
        except Exception:
            pass
        finally:
            user32.CloseClipboard()
        return ""
