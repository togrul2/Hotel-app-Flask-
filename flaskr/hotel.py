import math
from flask import Blueprint, render_template, request
from flaskr.db import get_db

bp = Blueprint('hotel', __name__)


@bp.route('/hotels/')
def hotels():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)
    db = get_db()
    num_of_hotels = db.execute("SELECT COUNT(*) FROM hotel").fetchone()[0]

    num_of_pages = math.ceil(num_of_hotels / per_page)
    offset = (page - 1) * per_page
    hotels_collection = db.execute("SELECT * FROM hotel LIMIT ? OFFSET ?", (per_page, offset)).fetchall()

    data = {
        'hotels': hotels_collection,
        'page': page,
        'num_of_pages': num_of_pages
    }
    return render_template('hotel/hotels.html', **data)


# @bp.route('/create-hotel', methods=['GET', 'POST'])
# @admin_required
# def create_hotel():
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         location = request.form['location']
#
#         if not (name and location):
#             abort(400, "All required fields must be filled")
#
#         try:
#             db = get_db()
#             db.execute("INSERT INTO hotel(name, description, location) VALUES (?, ? ,?)", (name, description, location))
#             db.commit()
#         except Exception as e:
#             print(e)
#
#         return redirect(url_for('hotel.hotels'))
#
#     return render_template('hotel/create-hotel.html')
