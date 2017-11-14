import hashlib
from .helpers import base_encoding, sanitize_url
from flask import current_app


MAX_ITERATION_COLLISION = 100
MIN_SHORT_URL_SIZE = 7
MAX_SHORT_URL_SIZE = 8


def hash_url(url_long):
    """
    Transform a url in a base 62 string by hashing it through md5, and converting the result in base 62
    """
    hexDigest = hashlib.md5(url_long.encode('utf-8')).hexdigest()
    return base_encoding(int(hexDigest, 16))


def _handle_collision(url_long, db):
    """
    Function used in case the short hashed version of a long url collides with an entry
    already existing in the storage.
    The new short url is generated as in hash_url by encoding in base 62 the hexdigest of a md5 hash
    of the long url, with the exception that the base 10 of its hexdigest is being divided by an
    increasing value until we don't have anymore collision, with up to MAX_ITERATION_COLLISION tries.
    returns None in case we can't find a value not colliding, the short url otherwise
    """
    hexDigest = hashlib.md5(url_long.encode('utf-8')).hexdigest()
    base_10_of_digest = int(hexDigest, 16)
    url_long_existing = url_long
    padding = 1
    url_short = None
    while (url_long_existing is not None) and (padding <= MAX_ITERATION_COLLISION):
        url_short = base_encoding(base_10_of_digest // padding)[:MIN_SHORT_URL_SIZE]
        url_long_existing = db.get_long_url()
        padding += 1
    return url_short if url_long_existing is None else None


def shorten_and_handle_url(url_long, db):
    """
    Try to get the short version of a long url by checking first if the long url has already been hashed before,
    if this is not the case, then try to hash it making sure to avoid collisions both due to the size of the short url
    and due to the md5 collisions that could happen.
    :param str url_long: the url to shorten
    :param DB db: the database object used for inserting and getting value to/from storage
    """
    # TODO: batch get items for better performances
    sanitized_url_to_shorten = sanitize_url(url_long)
    hashed_url = hash_url(sanitized_url_to_shorten)
    url_long_existing = None

    current_url_short_size = min(MIN_SHORT_URL_SIZE, len(hashed_url))
    url_short = hashed_url[:current_url_short_size]

    # Check short string collision
    while (url_long_existing != sanitized_url_to_shorten) \
        and (current_url_short_size < len(hashed_url)) \
            and (current_url_short_size < MAX_SHORT_URL_SIZE):
        current_app.logger.info('getting old url new row')
        url_long_existing = db.get_long_url(url_short)
        # It's the first time we input this short url
        if url_long_existing is None:
            db.insert_url(url_short, sanitized_url_to_shorten)
            current_app.logger.info('Inserting new row')
            break
        # There is already an existing short url for different long url, we try to increase the short url size
        elif url_long_existing != sanitized_url_to_shorten:
            current_url_short_size += 1
        # The entry exist for this long url
        else:
            break

    # If we still collide when increasing the size of the short url, we handle hash collision
    if (current_url_short_size >= len(hashed_url)) or (current_url_short_size >= MAX_SHORT_URL_SIZE):
        current_app.logger.warning(f"Collision happened for {sanitized_url_to_shorten}")
        url_short = _handle_collision(sanitized_url_to_shorten, db)
        if url_short is not None:
            db.insert_url(url_short, sanitized_url_to_shorten)

    return url_short
