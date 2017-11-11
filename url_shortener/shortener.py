import hashlib
from .helpers import base_encoding


def hash_url(url_long):
    hexDigest = hashlib.md5(url_long.encode('utf-8')).hexdigest()
    return base_encoding(int(hexDigest, 16))
