from flask import Flask, render_template, url_for, request, redirect
import flask
from .shortener import hash_url
from .db import DB

app = Flask(__name__)


@app.before_request
def init_db():
    if not hasattr(flask.g, 'database'):
        flask.g.database = DB(endpoint_url='http://dynamodb:8000', name_url_table='urls')
        app.logger.info('Creating database connection')
        flask.g.database.init_db()


@app.route('/')
def index():
    return render_template('index.html.j2', api_url=url_for('shorten_url'))


@app.route('/<url_short>', methods=['GET', ])
def redirect_short_url(url_short):
    long_url = flask.g.database.get_long_url(url_short)
    app.logger.info(f'Redirecting to {long_url}')
    if long_url is None:
        return redirect(url_for('index'))
    return redirect(long_url)


@app.route('/api/shorten', methods=['POST', ])
def shorten_url():
    long_url_to_shorten = request.form['url_long']
    hashed_url = hash_url(long_url_to_shorten)
    long_url_existing = None
    short_url_size = min(7, len(hashed_url))
    short_url = hashed_url[:short_url_size]

    try:
        # Check short string collision, TODO: collisions on md5
        while (long_url_existing != long_url_to_shorten) and (short_url_size < len(hashed_url)):
            app.logger.info('getting old url new row')
            long_url_existing = flask.g.database.get_long_url(short_url)
            # It's the first time we input this short url
            if long_url_existing is None:
                flask.g.database.insert_url(short_url, long_url_to_shorten)
                app.logger.info('Inserting new row')
                break
            # There is already an existing short utl for different long url
            elif long_url_existing != long_url_to_shorten:
                short_url_size += 1
            # The entry exist for this long url
            else:
                break
    except Exception as e:
        app.logger.error('Impossible to shorten the url because of a database problem', e)
        # flask.flash('Server error, please retry later', category='warning')
        return render_template('index.html.j2')

    return f"Your short URL for {long_url_to_shorten} is {short_url}.\n"
