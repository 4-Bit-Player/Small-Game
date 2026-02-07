


def decode_from_string(data:str):
    """
    Small decode function.\n
    Only works with strings that got encoded with my small string encoder.
    !!! Does NOT work with the byte encoding !!!
    :param data: The encoded string.
    :return: Whatever the string was before it got encoded.
    """
    t = type(data)

    if t == str:
        if len(data) == 0:
            return ""
        start_char = ord(data[0])
        if start_char < 125:
            val, _ = _lookup_table[start_char](data, 1)
            return val
        raise ValueError("Invalid start char!")


    err_msg = "Invalid type to decode: " + str(type(data))
    raise ValueError(err_msg)


def _decode_from_string(data:str):
    """
    Fall back function for the byte decoder.
    """
    if len(data) == 0:
        return ""
    start_char = ord(data[0])
    if start_char < 125:
        val, _ = _lookup_table[start_char](data, 1)
        return val
    raise ValueError("Invalid start char!")





def _dec_list(data, offset) -> tuple[list, int]:
    start = offset
    out = []
    while data[start] != "]":
        char = ord(data[start])
        val, start = _lookup_table[char](data, start + 1)
        out.append(val)
        continue
    return out, start+1



def _dec_tuple(data, offset) -> tuple[tuple, int]:
    start = offset
    out = []
    while data[start] != ")":
        char = ord(data[start])
        val, start = _lookup_table[char](data, start+1)
        out.append(val)
        continue
    return tuple(out), start+1


def _dec_set(data, offset) -> tuple[set, int]:
    start = offset
    out = []
    while data[start] != ">":
        char = ord(data[start])
        val, start = _lookup_table[char](data, start + 1)
        out.append(val)
        continue
    return set(out), start+1


def _dec_dict(data:str, offset:int) -> tuple[dict, int]:
    start = offset
    out:dict = {}
    while data[start] != "}":

        char = ord(data[start])
        key, start = _lookup_table[char](data, start + 1)
        char = ord(data[start])
        val, start = _lookup_table[char](data, start+1)
        out[key] = val

    return out, start+1


def _dec_num(data:str, offset:int) -> tuple[int | float, int]:
    """
    :return: returns the value and the new offset
    """
    end = data.find("\3", offset)
    num = data[offset-1:end]
    if "." in num:
        return float(num), end+1
    return int(num), end+1,


def _dec_string(data:str, offset:int) -> tuple[str, int]:
    end = data.find('"\3', offset)
    return data[offset:end], end + 2

def _dec_bytes(data:str, offset:int) -> tuple[bytes, int]:
    end = data.find('"\3', offset)
    return data[offset:end].encode(), end + 2

def _dec_none(data:str, offset:int) -> tuple[None, int]:
    return None, offset

def _dec_true(data:str, offset:int) -> tuple[bool, int]:
    return True, offset

def _dec_false(data:str, offset:int) -> tuple[bool, int]:
    return False, offset

def _dec_types(data:str, offset:int) -> tuple[type, int]:
    return _type_decode_lookup_table[data[offset]], offset+1


_lookup_table = [_dec_num for _ in range(125)]
_lookup_table[ord("{")] = _dec_dict
_lookup_table[ord("[")] = _dec_list
_lookup_table[ord("<")] = _dec_set
_lookup_table[ord("(")] = _dec_tuple
_lookup_table[ord('"')] = _dec_string
_lookup_table[ord('N')] = _dec_none
_lookup_table[ord('T')] = _dec_true
_lookup_table[ord('F')] = _dec_false
_lookup_table[ord('B')] = _dec_bytes
_lookup_table[ord('t')] = _dec_types

_type_decode_lookup_table = {
    "0":list,
    "1":dict,
    "2":set,
    "3":tuple,
    "4":int,
    "5":float,
    "6":str,
    "7":bool,
    "8":type,
    "9":bytes,
    "a":type(None),
}