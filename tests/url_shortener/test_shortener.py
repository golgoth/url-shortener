from url_shortener import shortener


def test_base_62_encode():
    assert shortener.hash_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ') == '3yWDLBXyfB8lnAfRFGXBod'
