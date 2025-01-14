from flask import Flask, session, render_template
from flask_session import Session
from flask_socketio import SocketIO
from redis import Redis
from dotenv import load_dotenv
from markupsafe import escape

import os.path


load_dotenv()

app = Flask(__name__)

SESSION_TYPE = 'redis'
SESSION_REDIS = Redis(host='localhost', port=8000)
app.config.from_object(__name__)
Session(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set/')
def session_set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def session_get():
    return session.get('key', 'not set')


if __name__ == '__main__':
    app.run(debug=True)
