import os


class Config(object):
    """Parent configuration class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://eKAdS9:XSe_8F1nfFAVT@utm_db/utm'


class DevelopmentConfig(Config):
    """Configurations for Development."""

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'mysecret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aaaa@localhost/db-project'
    SESSION_TYPE = 'sqlalchemy'
    DEBUG = True
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    JWT_SECRET_KEY = 'zbdxi$lpk@p)!)7s+vs(%+u!cthy)m9836g&^7paf8kiey&d@s'
    ACTIVATION_EXPIRE_DAYS = 15


class ProductionConfig(Config):
    """Configurations for Production."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://eKAdS9:XSe_8F1nfFAVT@utm_db/utm'
    DEBUG = False
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    JWT_SECRET_KEY = 'zbdxi$lpk@p)!)7s+vs(%+u!cthy)m9836g&^7paf8kiey&d@s'
    ACTIVATION_EXPIRE_DAYS = 15


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
