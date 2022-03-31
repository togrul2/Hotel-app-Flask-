from sqlite3 import IntegrityError

from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template('admin/index.html')


@bp.route('/hotels')
@admin_required
def hotels():
    # TODO implement pagination
    db = get_db()
    hotel_models = db.execute("SELECT * FROM hotel")

    data = {
        'hotels': hotel_models
    }
    return render_template('admin/hotels.html', **data)


@bp.route('/hotel-delete/<int:pk>')
@admin_required
def hotel_delete(pk):
    db = get_db()
    db.execute('DELETE FROM hotel WHERE id=?', (pk,))
    db.commit()

    return redirect(url_for('admin.hotels'))


@bp.route('/create-hotel', methods=['GET', 'POST'])
@admin_required
def create_hotel():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']

        if not (name and location):
            abort(400, "All required fields must be filled")
        try:
            db = get_db()
            db.execute("INSERT INTO hotel(name, description, location) VALUES (?, ? ,?)", (name, description, location))
            db.commit()
        except IntegrityError as e:
            print(e)

        return redirect(url_for('admin.hotels'))

    return render_template('admin/create-hotel.html')


@bp.route('/users')
@admin_required
def users():
    db = get_db()
    users_collection = db.execute("SELECT * from user").fetchall()

    data = {
        'users': users_collection
    }
    return render_template('admin/users.html', **data)


@bp.route('/create_superuser', methods=['GET', 'POST'])
@admin_required
def create_superuser():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        is_admin = request.form['is_admin']
        error = None

        if is_admin == 'true':
            is_admin = True
        else:
            is_admin = False

        # Checking are there unfilled fields
        if not all([username, email, password, confirm_password]):
            error = 'All required fields must be fulfilled'

        if password != confirm_password:
            error = 'Passwords do not match'

        if error is None:
            try:
                db.execute('INSERT INTO user(username, email, password, isAdmin) values (?, ?, ?, ?)', (username, email, password, is_admin))
                db.commit()
            except IntegrityError:
                error = f'User with the username {username} already exists'
            else:
                flash('User was successfully created', 'success')
                return redirect(url_for('admin.users'))

        flash(error)
    return render_template('admin/create-superuser.html')
