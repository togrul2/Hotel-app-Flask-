import functools
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None:
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        db = get_db()
        error = None

        if not username or not password:
            error = 'Username and password are required.'

        if password != confirm_password:
            error = 'Passwords do not match.'

        usernames = [i['upper_username'] for i in db.execute('SELECT upper(username) upper_username FROM user').fetchall()]

        if username.upper() in usernames:
            error = f'User with the username {username} already exists'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db.commit()
                pass
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash('User has been successfully created', 'success')
                return redirect(url_for("auth.login"))

        flash(message=error, category='danger')

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    redirect_link = url_for('homepage')
    if g.user is not None:
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if user['isAdmin']:
                redirect_link = url_for('admin.dashboard')
            return redirect(redirect_link)

        flash(message=error, category='danger')

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/logout')
@login_required
def logout():
    args = request.args
    redirect_link = args.get('next', url_for('homepage'))
    session.clear()
    return redirect(redirect_link)


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or bool(g.user['isAdmin']) is False:
            flash('You need to be authorized as an admin for this action', category='danger')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
