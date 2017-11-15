from flask import Flask, render_template, url_for, request, redirect, flash
import flask
from .shortener import shorten_and_handle_url
from .db import DB
import os
from urllib.parse import urlparse


app = Flask(__name__)
app.secret_key = os.urandom(24)

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
@app.route('/api/shorten', methods=['GET', ])
def index():
    return render_template('index.html.j2', api_url=url_for('shorten_url'))


@app.route('/<url_short>', methods=['GET', ])
def redirect_short_url(url_short):
    long_url = flask.g.database.get_long_url(url_short)
    # for urls without the http:// part, we add it, if the domain requires https it should redirect
    long_url = f'http://{long_url}' if urlparse(long_url).netloc =='' else long_url
    app.logger.info(f'Redirecting to {long_url}')
    if (long_url is None):
        flash('This url was not registered')
        return redirect(url_for('index'))
    return redirect(long_url)


@app.route('/api/shorten', methods=['POST', ])
def shorten_url():
    long_url_to_shorten = request.form['url_long']
    if long_url_to_shorten is None:
        flash('Incorrect input, please verify that you input a url to shorten', category='warning')
        return render_template('index.html.j2')
    try:
        short_url = shorten_and_handle_url(long_url_to_shorten, flask.g.database)
        assert short_url is not None
    except Exception as e:
        app.logger.error('Impossible to shorten the url because of a database problem', e)
        flash('Server error, please retry later', category='warning')
        return render_template('index.html.j2')

    short_url = request.headers['host'] + f'/{short_url}'
    return render_template('index.html.j2', api_url=url_for('shorten_url'), short_url=short_url)
