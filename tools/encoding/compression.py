import zlib


def compress_data(data, compression_level=-1):
    return zlib.compress(data, level=compression_level)


def decompress_data(compressed_data):
    return zlib.decompress(compressed_data)
