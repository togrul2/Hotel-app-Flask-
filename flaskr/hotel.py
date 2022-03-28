from flask import Blueprint, render_template

bp = Blueprint('hotel', __name__)


@bp.route('/hotels/')
def hotels():
    return render_template('hotel/hotels.html')
