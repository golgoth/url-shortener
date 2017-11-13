# note that with this base 62 elements, we can get weird urls
BASE_62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# (bad words or complex 0Oi1l -type strings)



def base_encoding(to_encode: int, base=BASE_62, length_base=len(BASE_62)):
    """
    :param to_encode: int in base 10 to Encode
    Encode an int to a base whose list of elements in order is <base>
    :param str base: string consisting of a list of unique elements ordered of the base.
    """
    if to_encode < length_base:
        return base[to_encode]
    return base_encoding(to_encode // length_base, base, length_base) + base[to_encode % length_base]


def sanitize_url(long_url):
    # TODO
    return long_url
