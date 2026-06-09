# byte encoder V1

# next free: b"\x18"

def encode_to_bytes(data) -> bytes:
    f"""
    Small encoder to encode almost all basic types into bytes. 
    Supported are:
    Float, Int, Str, None, Bool, list, dict, tuple, set, bytes, build in types 
    
    Not supported are:
    Custom types and circular nested structs

    (Encoding single values and not structs will most likely be larger than strings.)
    """
    _encode_lookup_table = get_byte_encode_lookup_table()
    result: list[bytes] = []
    _encode_lookup_table[type(data)](data, result, _encode_lookup_table)

    return b"".join(result)


def _enc_dict(data: dict, result: list[bytes], _encode_lookup_table:dict):
    result.append(b"\x0b")
    for key, val in data.items():
        _encode_lookup_table[type(key)](key, result, _encode_lookup_table)
        _encode_lookup_table[type(val)](val, result, _encode_lookup_table)
    result.append(b"\x0c")


def _enc_list(data: list, result: list[bytes], _encode_lookup_table:dict):
    result.append(b"\x0d")
    for val in data:
        _encode_lookup_table[type(val)](val, result, _encode_lookup_table)
    result.append(b"\x0e")


def _enc_set(data: set, result: list[bytes], _encode_lookup_table:dict):
    result.append(b"\x0f")
    for key in data:
        _encode_lookup_table[type(key)](key, result, _encode_lookup_table)
    result.append(b"\x10")


def _enc_tuple(data: tuple, result: list[bytes], _encode_lookup_table:dict):
    result.append(b"\x11")
    for val in data:
        _encode_lookup_table[type(val)](val, result, _encode_lookup_table)
    result.append(b"\x12")


def _enc_bool(val:bool, result: list[bytes], _encode_lookup_table:dict):
    if val:
        return result.append(b"\x01")
    return result.append(b"\x00")

def _enc_none(val:None, result: list[bytes], _encode_lookup_table:dict):
    return result.append(b"\x02")

def _enc_str(val:str, result: list[bytes], _encode_lookup_table:dict):
    """
    String encoding:
    For a length up to 255 bytes:
    First Byte : Saying that it's a short string
    Second Byte: Byte Length of the string

    If longer than 255 bytes:
    First Byte : Long string
    Second Byte: Byte Length of the number with the size of the string
    N Bytes: The number with the size of the string

    """


    bts = val.encode("utf-8")
    length = len(bts)

    if length <= 255:
        result.append(b"\x03" + length.to_bytes(1, byteorder="big") + bts)
        return

    req_bytes = (length.bit_length() + 7) // 8
    result.append(b"\x04" + req_bytes.to_bytes(1, byteorder="big") + length.to_bytes(req_bytes, byteorder="big") + bts)
    return


def _enc_int(val:int, result: list[bytes], _encode_lookup_table:dict):
    """
    Works similar to the string encoding.
    First byte tells either long or short negative or positive int.

    If it's a short int (negative doesn't matter):
    The second byte tells how many bytes are used to encode the int.
    Third onward is the int.

    If it's a large int (negative doesn't matter):
    Second byte tells the byte count of the size int.
    Third byte to n is the size of the int.

    """
    is_negative = False
    if val < 0:
        val = -val
        is_negative = True

    size = (val.bit_length() + 7) // 8

    if size <= 255:
        if is_negative:
            result.append(b"\x13" + size.to_bytes(1, byteorder="big") + val.to_bytes(size, byteorder="big"))
        else:
            result.append(b"\x05" + size.to_bytes(1, byteorder="big") + val.to_bytes(size, byteorder="big"))
        return

    # Looorge number O_o

    req_bytes = (size.bit_length() + 7) // 8

    if is_negative:
        result.append(b"\x14" + req_bytes.to_bytes(1, byteorder="big") + size.to_bytes(req_bytes, byteorder="big") + val.to_bytes(size, byteorder="big"))
    else:
        result.append(b"\x06" + req_bytes.to_bytes(1, byteorder="big") + size.to_bytes(req_bytes, byteorder="big") + val.to_bytes(size, byteorder="big"))



def _enc_float(val:float, result: list[bytes], _encode_lookup_table:dict):
    is_negative = False
    if val < 0:
        val = -val
        is_negative = True

    val, divider = val.as_integer_ratio()

    size = val.bit_length()
    if size <= 255:
        if is_negative:
            result.append(b"\x15" + divider.bit_length().to_bytes(1, byteorder="big") + size.to_bytes(1, byteorder="big") + val.to_bytes(size, byteorder="big"))
        else:
            result.append(b"\x07" + divider.bit_length().to_bytes(1, byteorder="big") + size.to_bytes(1, byteorder="big") + val.to_bytes(size, byteorder="big"))
        return

    # Looorge number O_o

    req_bytes = (size.bit_length() + 7) // 8

    if is_negative:
        result.append(b"\x16" + req_bytes.to_bytes(1, byteorder="big") + size.to_bytes(req_bytes, byteorder="big") + val.to_bytes(size, byteorder="big"))
    else:
        result.append(b"\x17" + req_bytes.to_bytes(1, byteorder="big") + size.to_bytes(req_bytes, byteorder="big") + val.to_bytes(size, byteorder="big"))





def _enc_bytes(val: bytes, result: list[bytes], _encode_lookup_table:dict):
    size = len(val)

    if size <= 255:
        result.append(b"\x08" + size.to_bytes(1, byteorder="big") + val)
        return

    req_bytes = (size.bit_length() + 7) // 8
    result.append(b"\x09" +
                  req_bytes.to_bytes(1, byteorder="big") +
                  size.to_bytes(req_bytes, byteorder="big") +
                  val)
    return


def _enc_type(val: type, result: list[bytes], _encode_lookup_table:dict):
    result.append(b"\x0a" + _type_encode_lookup_table[val])


_type_encode_lookup_table = {
    list: b"\x00",
    dict: b"\x01",
    set: b"\x02",
    tuple: b"\x03",
    int: b"\x04",
    float: b"\x05",
    str: b"\x06",
    bool: b"\x07",
    type: b"\x08",
    bytes: b"\x09",
    type(None):b"\x0a",
}

def get_byte_encode_lookup_table() -> dict:
    return {
    list: _enc_list,
    dict: _enc_dict,
    set: _enc_set,
    tuple: _enc_tuple,
    int: _enc_int,
    float: _enc_float,
    str: _enc_str,
    bool: _enc_bool,
    type(None): _enc_none,
    bytes: _enc_bytes,
    type: _enc_type,
}