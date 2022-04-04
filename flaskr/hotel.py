import math
from flask import Blueprint, render_template, request, current_app
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
    search_query = """SELECT * FROM hotel LIMIT ? OFFSET ?"""
    hotels_collection = db.execute(search_query, (per_page, offset)).fetchall()

    data = {
        'hotels': hotels_collection,
        'page': page,
        'num_of_pages': num_of_pages
    }
    return render_template('hotel/hotels.html', **data)
