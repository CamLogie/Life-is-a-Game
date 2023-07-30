import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from life_is_a_game.db import get_db, close_db, results_to_dict
from life_is_a_game.profile import load_user_wallet


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register new user"""
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
                cur.execute('''
                    INSERT INTO users (username, password, first_name, last_name) 
                    VALUES %s
                    RETURNING id, username
                ;''', [(username, generate_password_hash(password), first_name, last_name)],
                )
                user_data = results_to_dict(cur)
                create_wallet(cur, db, user_data)
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                close_db(db, cur)
                return redirect(url_for("auth.login"))
        
        flash(error)        

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """log in user"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        db = get_db()
        cur = db.cursor()
        cur.execute('''SELECT * FROM users WHERE username = %s''', (username,))

        user = results_to_dict(cur)

        close_db(db, cur)

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('profile.wallet'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """Set global user to current user if user is signed in otherwise set to None"""
    user_id = session.get('user_id')
    db = get_db()
    cur = db.cursor()

    if user_id is None:
        g.user = None
    else:
        cur.execute('''SELECT * FROM users WHERE id = %s''', (user_id,))
        g.user = results_to_dict(cur)
        g.user_wallet = load_user_wallet(cur, user_id)
    
    close_db(db, cur)
    
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

def create_wallet(cur, conn, user_data):
    cur.execute('''
        INSERT INTO wallet (user_id, username, health_points_balance, life_points_balance, money_points_balance)
        VALUES (%s, %s, 0, 0, 0)
        ;''', (user_data['id'], user_data['username'])
    )
    conn.commit()



