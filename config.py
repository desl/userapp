import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/flask-heroku'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    DEBUG = True
    ['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-migrate-users'
    
class TestingConfig(Config):
    TESTING = True