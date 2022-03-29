from flask import Blueprint, render_template, request, abort, redirect, url_for

from flaskr.auth import is_admin
from flaskr.db import get_db

bp = Blueprint('hotel', __name__)


@bp.route('/hotels/')
def hotels():
    db = get_db()
    hotels_collection = db.execute("SELECT * FROM hotel").fetchall()
    data = {
        'hotels': hotels_collection
    }
    return render_template('hotel/hotels.html', **data)


@bp.route('/create-hotel', methods=['GET', 'POST'])
@is_admin
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
        except Exception as e:
            print(e)

        return redirect(url_for('hotel.hotels'))

    return render_template('hotel/create-hotel.html')
