from url_shortener import helpers


def test_base_62_encode():
    assert helpers.base_encoding(61) == 'Z'
    assert helpers.base_encoding(0) == '0'
    assert helpers.base_encoding(62) == '10'
    assert helpers.base_encoding(134) == '1a'
