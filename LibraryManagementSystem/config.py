import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # SECRET_KEY = b'\xed\xd47\x83\xaf\xeb*\xd1\xe1Y\x89e\xfc\xb0E\xb2\xc5\x9d\x1d/\xe8\xbf\xc7\xc9'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost/Library'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True