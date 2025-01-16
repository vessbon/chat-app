from flask import Flask, session, render_template, url_for, redirect
from flask_session import Session
from flask_socketio import SocketIO
from functools import wraps
from redis import Redis
from dotenv import load_dotenv
from markupsafe import escape


# ---> ENVIRONMENT
load_dotenv()

# ---> APP
app = Flask(__name__)
app.secret_key = 'PAFja89wfaIUO'

SESSION_TYPE = 'redis'
SESSION_REDIS = Redis(host='localhost', port=8000)
app.config.from_object(__name__)
Session(app)


# ---> MIDDLEWARE
#  Authentication check
def require_auth(original_function):
    @wraps(original_function)
    def decorated_function(*args, **kwargs):
        if 'auth' not in session or not session['auth']:
            return redirect(url_for('login'))
        return original_function(*args, *kwargs)
    return decorated_function

# Admin check
def require_admin(original_function):
    @wraps(original_function)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('forbidden'))
        return original_function(*args, *kwargs)
    return decorated_function


# ---> ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
@require_auth
@require_admin
def dashboard():
    pass


# ---> LOGIC
if __name__ == '__main__':
    app.run(debug=True)
