import os
from . import db, auth, hotel, config

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevConfig)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.db'),
    )

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

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(hotel.bp)
    app.add_url_rule('/', endpoint='hotel')

    return app
