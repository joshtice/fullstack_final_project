import os

DEBUG = False
REDIRECT_URI = os.environ.get('REDIRECT_URI', '')
SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', '')