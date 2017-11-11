from flask import Flask, render_template, url_for, request
import flask
from .shortener import hash_url
from .db import DB

app = Flask(__name__)


@app.route('/')
def index():
    if not hasattr(flask.g, 'database'):
        flask.g.database = DB(endpoint_url='http://localhost:8000', name_url_table='urls')

    return render_template('index.html.j2', api_url=url_for('shorten_url'))


@app.route('/api/shorten', methods=['POST', ])
def shorten_url():
    long_url_to_shorten = request.form['url_long']
    hashed_url = hash_url(long_url_to_shorten)
    long_url_existing = None
    initial_short_url_size = 7
    short_url = hashed_url[:initial_short_url_size]

    try:
        # Check short string collision, TODO: collisions on md5
        while long_url_existing != long_url_to_shorten:
            long_url_existing = flask.g.database.get_long_url(short_url)
            # It's the first time we input this short url
            if long_url_existing is None:
                flask.g.database.insert_url(hashed_url, long_url_to_shorten)
                break
            # There is already an existing short utl for different long url
            elif long_url_existing != long_url_to_shorten:
                initial_short_url_size += 1
            # The entry exist for this long url
            else:
                break
    except Exception:
        app.logger.error('Impossible to shorten the url because of a database problem')
        flask.flash('Server error, please retry later', category='warning')
        return render_template('index.html.j2')

    return f"Your short URL for {long_url_to_shorten} is {short_url}.\n"
