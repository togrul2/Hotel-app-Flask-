import math
import os
from sqlite3 import IntegrityError
from flask import current_app, jsonify
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from werkzeug.utils import secure_filename
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
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    num_of_hotels = db.execute("SELECT COUNT(*) FROM hotel").fetchone()[0]
    num_of_pages = math.ceil(num_of_hotels / per_page)
    offset = (page - 1) * per_page
    hotel_models = db.execute("SELECT * FROM hotel LIMIT ? OFFSET ?", (per_page, offset)).fetchall()

    data = {
        'hotels': hotel_models,
        'page': page,
        'num_of_pages': num_of_pages
    }
    return render_template('admin/hotels.html', **data)


@bp.route('/hotel-delete/<int:pk>')
@admin_required
def delete_hotel(pk):
    db = get_db()
    db.execute('DELETE FROM hotel WHERE id=?', (pk,))
    db.commit()

    return redirect(url_for('admin.hotels'))


@bp.route('/create-hotel', methods=['GET', 'POST'])
@admin_required
def create_hotel():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        images = request.files.getlist('images')

        if not (name and location):
            abort(400, "All required fields must be filled")
        try:
            db = get_db()
            db.execute("INSERT INTO hotel(name, description, location) VALUES (?, ? ,?)", (name, description, location))
            if len(images) > 0:
                hotel_id = db.execute("SELECT id FROM hotel WHERE name=? AND description=? AND location=?",
                                      (name, description, location)).fetchone()[0]
                for image in images:
                    if image.filename != '':
                        filename = f'{hotel_id}.{secure_filename(image.filename)}'
                        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                        db.execute("INSERT INTO hotel_image(hotel_id, source, description) VALUES (?, ?, ?)",
                                   (hotel_id, filename, ''))
            db.commit()
        except IntegrityError as e:
            flash(str(e), 'danger')

        return redirect(url_for('admin.hotels'))

    return render_template('admin/create-hotel.html')


@bp.route('/edit-hotel/<int:pk>', methods=['GET', 'POST'])
@admin_required
def edit_hotel(pk):
    db = get_db()
    hotel = db.execute('SELECT * FROM hotel WHERE id=?', (pk,)).fetchone()
    images = db.execute('SELECT * FROM hotel_image WHERE hotel_id=?', (pk,)).fetchall()
    context = {
        'hotel': hotel,
        'images': images
    }
    if request.method == 'POST':
        pass
    return render_template('admin/edit_hotel.html', **context)


@bp.route('/delete-image/<int:pk>', methods=['DELETE'])
def delete_image(pk):
    db = get_db()
    db.execute('DELETE FROM hotel_image WHERE id=?', (pk,))
    db.commit()
    return jsonify({'status': 'OK', 'message': f'Image with id {pk} was successfully deleted'})


@bp.route('/users')
@admin_required
def users():
    db = get_db()
    users_collection = db.execute("SELECT * from user").fetchall()

    data = {
        'users': users_collection
    }
    return render_template('admin/users.html', **data)


@bp.route('/create-superuser', methods=['GET', 'POST'])
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

        usernames = db.execute('SELECT upper(username) FROM user').fetchall()
        if username.upper() in usernames:
            error = f'User with the username {username} already exists'

        if error is None:
            try:
                db.execute('INSERT INTO user(username, email, password, isAdmin) values (?, ?, ?, ?)',
                           (username, email, password, is_admin))
                db.commit()
            except IntegrityError:
                error = f'User with the username {username} already exists'
            else:
                flash('User was successfully created', 'success')
                return redirect(url_for('admin.users'))

        flash(error)
    return render_template('admin/create-superuser.html')


@bp.route('/edit-user/<int:pk>', methods=['GET', 'POST'])
@admin_required
def edit_superuser(pk):
    db = get_db()
    user_to_edit = db.execute("SELECT username, email, isAdmin FROM user WHERE id=?", (pk,)).fetchone()
    context = {'user': user_to_edit}

    return render_template('admin/edit-superuser.html', **context)
