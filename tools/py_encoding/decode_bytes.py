from .decoding import _decode_from_string


def decode_from_bytes(data:bytes):
    """
    Small byte decode function.

    Only works with bytes that got encoded with my small byte encoder.
    Tries to fall back to the string decoder if the input is a string or the start byte is incorrect.

    :param data: The encoded bytes.
    :return: Whatever the bytes were before it got encoded.
    """
    t = type(data)
    if t == bytes:
        if len(data) == 0:
            return b""
        index = data[0]
        if index <= _highest_num:
            val, _ = _lookup_table[index](data, 1)
            return val

        try:
            return _decode_from_string(data.decode("utf-8"))

        except (ValueError, IndexError) as e:
            pass

        raise ValueError("Invalid start char!")


    if t == str:
        try:
            return _decode_from_string(data)
        except (ValueError, IndexError) as e:
            pass


    err_msg = "Invalid type to decode: " + str(t)
    raise ValueError(err_msg)



def _dec_list(data:bytes, offset: int) -> tuple[list, int]:
    start = offset
    out = []
    end_num = int.from_bytes(b"\x0e", byteorder="big")
    while data[start] != end_num:
        index = data[start]
        val, start = _lookup_table[index](data, start + 1)
        out.append(val)
        continue
    return out, start+1


def _dec_tuple(data:bytes, offset: int) -> tuple[tuple, int]:
    start = offset
    out = []
    end_num = int.from_bytes(b"\x12", byteorder="big")
    while data[start] != end_num:
        index = data[start]
        val, start = _lookup_table[index](data, start+1)
        out.append(val)
        continue
    return tuple(out), start+1


def _dec_set(data:bytes, offset: int) -> tuple[set, int]:
    start = offset
    out = []
    end_num = int.from_bytes(b"\x10", byteorder="big")
    while data[start] != end_num:
        index = data[start]
        val, start = _lookup_table[index](data, start + 1)
        out.append(val)
        continue
    return set(out), start+1


def _dec_dict(data:bytes, offset: int) -> tuple[dict, int]:
    start = offset
    out:dict = {}
    end_num = int.from_bytes(b"\x0c", byteorder="big")
    while data[start] != end_num:

        index = data[start]
        key, start = _lookup_table[index](data, start + 1)
        index = data[start]
        val, start = _lookup_table[index](data, start + 1)
        out[key] = val

    return out, start+1


def _val_err(data:bytes, offset: int) -> tuple[int | float, int]:
    msg = f"Encountered unexpected byte at index {offset-1}!"
    raise ValueError(msg)


def _dec_short_string(data:bytes, offset: int) -> tuple[str, int]:
    length = data[offset]
    offset += 1
    text = data[offset:offset+length].decode("utf-8")

    return text, offset+length

def _dec_long_string(data:bytes, offset: int) -> tuple[str, int]:
    size_length = data[offset]
    offset += 1
    length = int.from_bytes(data[offset:offset+size_length], byteorder="big")
    offset += size_length
    text = data[offset:offset+length].decode("utf-8")

    return text, offset + length


def _dec_short_bytes(data:bytes, offset: int) -> tuple[bytes, int]:
    length = data[offset]
    offset += 1
    text = data[offset:offset+length]

    return text, offset + length


def _dec_long_bytes(data: bytes, offset: int) -> tuple[bytes, int]:
    size_length = data[offset]
    offset += 1
    length = int.from_bytes(data[offset:offset + size_length], byteorder="big")
    offset += size_length
    text = data[offset:offset + length]

    return text, offset + length


def _dec_short_int(data: bytes, offset: int) -> tuple[int, int]:
    length = data[offset]
    offset += 1
    num = int.from_bytes(data[offset : offset + length], byteorder="big")
    return num, offset + length


def _dec_short_negative_int(data: bytes, offset: int) -> tuple[int, int]:
    val, offset = _dec_short_int(data, offset)
    return -val, offset


def _dec_long_negative_int(data: bytes, offset: int) -> tuple[int, int]:
    val, offset = _dec_long_int(data, offset)
    return -val, offset


def _dec_long_int(data: bytes, offset: int) -> tuple[int, int]:
    size_length = data[offset]
    offset += 1
    length = 0
    length.from_bytes(data[offset:offset + size_length], byteorder="big")
    offset += size_length
    num = 0
    num.from_bytes(data[offset:offset + length], byteorder="big")

    return num, offset + length

def _dec_float(data: bytes, offset: int) -> tuple[float, int]:
    length = data[offset]
    offset += 1
    num = float(data[offset:offset + length])

    return num, offset + length


def _dec_none(data:bytes, offset:int) -> tuple[None, int]:
    return None, offset

def _dec_true(data:bytes, offset:int) -> tuple[bool, int]:
    return True, offset

def _dec_false(data:bytes, offset:int) -> tuple[bool, int]:
    return False, offset

def _dec_types(data:bytes, offset:int) -> tuple[type, int]:
    return _type_decode_lookup_table[data[offset]], offset+1

_highest_num = int.from_bytes(b"\x14")

_lookup_table = [_val_err for _ in range(_highest_num + 1)]
_lookup_table[int.from_bytes(b"\x00", byteorder="big")] = _dec_false
_lookup_table[int.from_bytes(b"\x01", byteorder="big")] = _dec_true
_lookup_table[int.from_bytes(b"\x02", byteorder="big")] = _dec_none
_lookup_table[int.from_bytes(b"\x03", byteorder="big")] = _dec_short_string
_lookup_table[int.from_bytes(b"\x04", byteorder="big")] = _dec_long_string
_lookup_table[int.from_bytes(b"\x05", byteorder="big")] = _dec_short_int
_lookup_table[int.from_bytes(b"\x06", byteorder="big")] = _dec_long_int
_lookup_table[int.from_bytes(b"\x07", byteorder="big")] = _dec_float
_lookup_table[int.from_bytes(b"\x08", byteorder="big")] = _dec_short_bytes
_lookup_table[int.from_bytes(b"\x09", byteorder="big")] = _dec_long_bytes
_lookup_table[int.from_bytes(b"\x0a", byteorder="big")] = _dec_types
_lookup_table[int.from_bytes(b"\x0b", byteorder="big")] = _dec_dict
_lookup_table[int.from_bytes(b"\x0d", byteorder="big")] = _dec_list
_lookup_table[int.from_bytes(b"\x0f", byteorder="big")] = _dec_set
_lookup_table[int.from_bytes(b"\x11", byteorder="big")] = _dec_tuple
_lookup_table[int.from_bytes(b"\x13", byteorder="big")] = _dec_short_negative_int
_lookup_table[int.from_bytes(b"\x14", byteorder="big")] = _dec_long_negative_int

_type_decode_lookup_table = {
    int.from_bytes(b"\x00"): list,
    int.from_bytes(b"\x01"): dict,
    int.from_bytes(b"\x02"): set,
    int.from_bytes(b"\x03"): tuple,
    int.from_bytes(b"\x04"): int,
    int.from_bytes(b"\x05"): float,
    int.from_bytes(b"\x06"): str,
    int.from_bytes(b"\x07"): bool,
    int.from_bytes(b"\x08"): type,
    int.from_bytes(b"\x09"): bytes,
    int.from_bytes(b"\x0a"): type(None),
}