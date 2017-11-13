from url_shortener import shortener
from url_shortener import helpers
from unittest.mock import MagicMock
from url_shortener.db import DB
from flask import Flask, current_app


def test_base_62_encode():
    assert shortener.hash_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ') == '3yWDLBXyfB8lnAfRFGXBod'

def test_handle_collision_max_iteration():
    mocked_db = DB('urls')
    mocked_db.get_long_url = MagicMock(return_value="d")
    short_url = shortener._handle_collision('old_url', mocked_db)
    db_call_count = mocked_db.get_long_url.call_count
    assert db_call_count == shortener.MAX_ITERATION_COLLISION, f'handle collision iterated a wrong number of times {db_call_count} instead of {shortener.MAX_ITERATION_COLLISION}'
    assert short_url is None

def test_handle_collision_return_short_url():
    mocked_db = DB('urls')
    mocked_db.get_long_url = MagicMock()
    mocked_db.get_long_url.side_effect = ['a', 'b', 'c', 'd', None]
    short_url_4_iteration = shortener._handle_collision('old_url', mocked_db)
    db_call_count = mocked_db.get_long_url.call_count
    assert db_call_count == 5, f'handle collision iterated a wrong number of times {db_call_count} instead of 5'

    mocked_db.get_long_url.side_effect = ['a', 'b', 'c', None]
    short_url_3_iteration = shortener._handle_collision('old_url', mocked_db)
    db_call_count = mocked_db.get_long_url.call_count
    assert short_url_4_iteration != short_url_3_iteration, f'The short url is the same for different iterations'


def test_shorten_url_should_handle_short_input():
    mocked_db = DB('urls')
    mocked_db.get_long_url = MagicMock(return_value=None)
    mocked_db.insert_url = MagicMock(return_value=None)
    app = Flask(__name__)
    with app.app_context():
        short_url = shortener.shorten_and_handle_url('a', mocked_db)
        assert len(short_url) > 0, f'<{short_url}> is incorrect'


def test_shorten_url_should_handle_new_short_url():
    mocked_db = DB('urls')
    mocked_db.get_long_url = MagicMock(return_value=None)
    mocked_db.insert_url = MagicMock(return_value=None)
    app = Flask(__name__)
    with app.app_context():
        short_url = shortener.shorten_and_handle_url('a', mocked_db)
        mocked_db.insert_url.assert_called_once()

def test_shorten_url_should_handle_collision_max_short_url_size_reached():
    mocked_db = DB('urls')
    mocked_db.get_long_url = MagicMock()
    mocked_db.get_long_url.side_effect = [str(i) for i in range(shortener.MAX_SHORT_URL_SIZE + 2)] + [None]
    mocked_db.insert_url = MagicMock(return_value=None)
    app = Flask(__name__)
    with app.app_context():
        short_url = shortener.shorten_and_handle_url('a', mocked_db)
        mocked_db.insert_url.assert_called_once()
