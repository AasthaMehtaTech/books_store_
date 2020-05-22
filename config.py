import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '0157'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


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
'''
Commands to run
    .\Scripts\activate
    python app.py
    set APP_SETTINGS="config.DevelopmentConfig"
    set DATABASE_URL="postgresql://localhost/books_store"
    >echo  %DATABASE_URL%
    pip install flask_sqlalchemy
    pip install flask_script
    pip install flask_migrate
    pip install psycopg2-binary
    python manage.py db init

        '''
