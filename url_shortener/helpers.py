BASE_62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def base_encoding(to_encode: int, base=BASE_62, length_base=len(BASE_62)):
    if to_encode < length_base:
        return base[to_encode]
    return base_encoding(to_encode // length_base, base, length_base) + base[to_encode % length_base]
