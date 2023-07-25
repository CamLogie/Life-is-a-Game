import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from life_is_a_game.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        db = get_db()
        cur = db.cursor()
        error = None

        if not username:
            error = 'Username is required'
        elif not password: 
            error = 'Password is required'
        elif not first_name:
            error = 'First name is required'
        elif not last_name:
            error = 'Last name is required'

        if error is None:
            try:
                cur.execute('INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), first_name, last_name),
                )
                cur.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        error = None
        user = cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db = get_db()
    cur = db.cursor()

    if user_id is None:
        g.user = None
    else:
        g.user = cur.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view