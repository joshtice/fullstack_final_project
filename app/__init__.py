import os

from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('config.default')

# Determine whether running development or production, and load 
# environment variables appropriately
app.config.from_envvar('APP_MODE')
if app.config['APP_MODE'] == 'development':
    app.config.from_object('config.developmenty')
    app.config.from_pyfile('instance_config.py')
elif app.config['APP_MODE' == 'production':
    app.config.from_object('config.production')
    app.config.from_envvar('SECRET_KEY')
    app.config.from_envvar('DATABASE_URL')


from app import views
