import sys, os
import zlib
from pathlib import Path
from pickle import loads

from tools.py_encoding import decode_from_bytes, encode_to_bytes



def _get_save_path() -> Path:
    home = Path.home()
    if sys.platform == "win32":
        return home / "AppData/Roaming" / "4 Bit Projects" / "Small Game"
    elif sys.platform.startswith("linux"):
        return home / ".local/share" / "4 Bit Projects" / "Small Game"
    elif sys.platform == "darwin":
        return home / "Library/Application Support" / "4 Bit Projects" / "Small Game"
    return home /  "4 Bit Projects" / "Small Game"



def save_game(save_num:int, data:dict) -> int:
    path = _get_save_path()
    if not path.exists():
        os.makedirs(path, exist_ok=True)
    file_path = path / f"save {save_num}"
    data2 = zlib.compress(encode_to_bytes(data))

    with open(file_path, "wb") as file:
        file.write(data2)

    return 0


def load_save(save_num:int):
    path = _get_save_path() / f"save {save_num}"
    if not path.exists():
        return ""

    with open(path, "rb") as file:
        data = file.read()
    try:
        save = decode_from_bytes(zlib.decompress(data))
        return save
    except zlib.error:
        pass

    try:
        save = loads(data)
        return save
    except MemoryError:
        return ""


def get_save_nums() -> list[int]:
    path = _get_save_path()
    if not path.exists() and path != "":
        return []

    files:list[int] = []
    for file in path.iterdir():
        if not file.is_file:
            continue
        file = str(file)
        if file.rfind("save ", len(file)-9) == -1:
            continue

        try:
            num = int(file[file.rfind(" ") + 1:])
            if num == -1:
                continue
            files.append(num)
        except ValueError:
            continue

    return files


def delete_save(save_num:int) -> None:
    path = _get_save_path() / f"save {save_num}"
    if path.exists():
        os.remove(path)