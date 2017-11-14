from flask import Flask, render_template, url_for, request, redirect
import flask
from .shortener import shorten_and_handle_url
from .db import DB

app = Flask(__name__)


@app.before_request
def init_db():
    if not hasattr(flask.g, 'database'):
        try:
            flask.g.database = DB(name_url_table='urls')
            app.logger.info('Creating database connection')
            flask.g.database.init_db()
        except Exception as e:
            app.logger.error('Failling creating table', e)


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
    try:
        short_url = shorten_and_handle_url(long_url_to_shorten, flask.g.database)
        assert short_url is not None
    except Exception as e:
        app.logger.error('Impossible to shorten the url because of a database problem', e)
        # flask.flash('Server error, please retry later', category='warning')
        return render_template('index.html.j2')

    short_url = request.headers['host'] + f'/{short_url}'
    return render_template('index.html.j2', api_url=url_for('shorten_url'), short_url=short_url)
