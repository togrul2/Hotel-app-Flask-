import os
from . import db, auth, hotel, config, admin
from flask import Flask, render_template

from .db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevConfig)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.db'),
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'uploads'),
        MAX_CONTENT_PATH=4096
    )

    @app.context_processor
    def utility_processor():
        def getImages(hotel_id):
            _db = get_db()
            return _db.execute('SELECT * FROM hotel_image WHERE hotel_id=?', (hotel_id,)).fetchall()
        return dict(getImages=getImages)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def page_not_found(e=None):
        return render_template('404.html'), 404

    app.register_error_handler(404, page_not_found)
    # app.register_error_handler(500, internal_server_error)

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(hotel.bp)
    app.register_blueprint(admin.bp)
    app.add_url_rule('/', endpoint='hotel')

    return app
