from flask import Flask, session, render_template, url_for, redirect, request
from flask_session import Session
from flask_socketio import SocketIO
from functools import wraps
from redis import asyncio as aioredis
from dotenv import load_dotenv
from markupsafe import escape
import bcrypt
import uuid_utils

from utils import getCredentials


# ---> ENVIRONMENT
load_dotenv()

# ---> APP
app = Flask(__name__)
app.secret_key = 'PAFja89wfaIUO'

SESSION_TYPE = 'redis'
SESSION_REDIS = aioredis.Redis(host='localhost', port=6379)
app.config.from_object(__name__)
Session(app)


# ---> MIDDLEWARE
#  Authentication check
def require_auth(original_function):
    @wraps(original_function)
    async def decorated_function(*args, **kwargs):
        if 'auth' not in session or not session['auth']:
            return redirect(url_for('login'))
        return await original_function(*args, *kwargs)
    return decorated_function

# Admin check
def require_admin(original_function):
    @wraps(original_function)
    async def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('forbidden'))
        return await original_function(*args, *kwargs)
    return decorated_function


# ---> USER CLASS
class User:
    pass


# ---> ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        credentials = await getCredentials(request.form)
    
    return await render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        credentials = await getCredentials(request.form)

        hashed_password = await bcrypt.hashpw(credentials['password'], 12)

        session['auth'] = True
        session['email'] = credentials['email']
        session['userId'] = str(uuid_utils.uuid7())
        
    
    return render_template('register.html')

@app.route('/dashboard')
@require_auth
@require_admin
async def dashboard():
    pass


# ---> LOGIC
if __name__ == '__main__':
    app.run(debug=True)
