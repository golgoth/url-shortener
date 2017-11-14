from url_shortener import db
from unittest.mock import MagicMock

def test_insert_url_should_insert_and_cache():
    fake_db = db.DB('test')
    fake_db.redis = MagicMock()
    fake_db.redis.set = MagicMock()

    url_table = MagicMock()
    url_table.put_item = MagicMock()
    fake_db.resource.Table = MagicMock(return_value=url_table)

    fake_db.insert_url('short', 'long')

    url_table.put_item.assert_called_once()
    fake_db.redis.set.assert_called_once()


def test_long_url_should_query_cache_and_return_existing_value():
    fake_db = db.DB('test')
    fake_db.redis = MagicMock()
    fake_db.redis.get = MagicMock(return_value=b'long')

    url_long = fake_db.get_long_url('short')

    fake_db.redis.get.assert_called_once()
    assert url_long == 'long'



def test_long_url_should_query_db_if_not_cached_and_cache_and_return_value():
    fake_db = db.DB('test')
    fake_db.redis = MagicMock()
    fake_db.redis.get = MagicMock(return_value=None)
    fake_db.redis.set = MagicMock()


    url_table = MagicMock()
    url_table.get_item = MagicMock(return_value={'Item': {'long_url': 'long'}})
    fake_db.resource.Table = MagicMock(return_value=url_table)

    url_long = fake_db.get_long_url('short')

    fake_db.redis.get.assert_called_once()
    fake_db.redis.set.assert_called_once()
    url_table.get_item.assert_called_once()
    assert url_long == 'long'

def test_long_url_should_return_None_if_no_corr_value_in_db():
    fake_db = db.DB('test')
    fake_db.redis = MagicMock()
    fake_db.redis.get = MagicMock(return_value=None)
    fake_db.redis.set = MagicMock()


    url_table = MagicMock()
    url_table.get_item = MagicMock(return_value={})
    fake_db.resource.Table = MagicMock(return_value=url_table)

    url_long = fake_db.get_long_url('short')

    fake_db.redis.set.assert_not_called()
    url_table.get_item.assert_called_once()
    assert url_long is None
