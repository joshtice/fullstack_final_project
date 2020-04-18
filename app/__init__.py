import os

from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('config.default')

# Determine whether running development or production, and load 
# environment variables appropriately
app.config['APP_MODE'] = os.environ.get('APP_MODE')
if app.config['APP_MODE'] == 'development':
    app.config.from_object('config.development')
    app.config.from_object('instance.config')
elif app.config['APP_MODE'] == 'production':
    app.config.from_object('config.production')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')

from app import views
