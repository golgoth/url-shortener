from flask import Flask, render_template, url_for, request


app = Flask(__name__)

@app.route('/')
def hello():
    count = redis.incr('hits')
    return render_template('index.html.j2', api_url=url_for('shorten_url'))


@app.route('/api/shorten', methods=['POST',])
def shorten_url():
    long_url = request.form['url_long']
    short_url = "hahahaha"
    return f"Your short URL for {long_url} is {short_url}.\n"
