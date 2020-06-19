import os

DEBUG = True
REDIRECT_URI = os.environ.get('DEV_REDIRECT_URI', '')
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', '')