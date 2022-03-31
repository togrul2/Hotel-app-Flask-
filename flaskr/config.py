"""Flask configuration."""


class Config:
    """Base config."""
    SECRET_KEY = 'a96207232cd1b9152989f650409750d5286c973c315af55b89536c21d9e76111'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
