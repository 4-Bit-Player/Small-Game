
# encoder V4

def encode_data(data) -> str:
    f"""
    Small encoder to encode almost all basic types. \n
    Supported are:\n
    Float, Int, Str, None, Bool, list, dict, tuple, set, byte string. \n
    Not supported are:\n
    Custom types and circular nested structs\n
    !!!Warning: Don't use a " followed by an unescaped \3 in your strings! \n
    It will lead to errors!!! \n

    (Encoding pure strings will be larger than the basic ones.)
    """

    result: list[str] = []
    _encode_lookup_table[type(data)](data, result)

    return "".join(result)


def _enc_dict(data: dict, result: list[str]):
    result.append("{")
    for key, val in data.items():
        _encode_lookup_table[type(key)](key, result)
        _encode_lookup_table[type(val)](val, result)
    result.append("}")


def _enc_list(data: list, result: list[str]):
    result.append("[")
    for val in data:
        _encode_lookup_table[type(val)](val, result)
    result.append("]")
    return


def _enc_set(data: set, result: list[str]):
    result.append("<")
    for key in data:
        _encode_lookup_table[type(key)](key, result)
    result.append(">")
    return


def _enc_tuple(data: tuple, result: list[str]):
    result.append("(")
    for val in data:
        _encode_lookup_table[type(val)](val, result)
    result.append(")")
    return


def _enc_bool_and_none(val, result: list[str]):
    result.append(str(val)[0])
    return


def _enc_str(val, result: list[str]):
    return result.append(f'"{val}"\3')


def _enc_num(val, result: list[str]):
    return result.append(f"{val}\3")


def _enc_bytes(data: bytes, result: list[str]):
    return result.append(f'B{data.decode()}"\3')


def _enc_type(val: type, result: list[str]):
    return result.append(f"t{_type_encode_lookup_table[val]}")


_encode_lookup_table = {
    list: _enc_list,
    dict: _enc_dict,
    set: _enc_set,
    tuple: _enc_tuple,
    int: _enc_num,
    float: _enc_num,
    str: _enc_str,
    bool: _enc_bool_and_none,
    type(None): _enc_bool_and_none,
    bytes: _enc_bytes,
    type: _enc_type,
}
_type_encode_lookup_table = {
    list: "0",
    dict: "1",
    set: "2",
    tuple: "3",
    int: "4",
    float: "5",
    str: "6",
    bool: "7",
    type: "8",
    bytes: "9",
    type(None):"a",
}