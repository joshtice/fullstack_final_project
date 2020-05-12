import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('config.default')

# Determine whether running development or production, and load 
# environment variables appropriately
app.config['APP_MODE'] = os.environ.get('APP_MODE')
if app.config['APP_MODE'] == 'development':
    app.config.from_object('config.development')
    app.config.from_object('instance.config')
elif app.config['APP_MODE'] == 'test':
    app.config.from_object('config.test')
elif app.config['APP_MODE'] == 'production':
    app.config.from_object('config.production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import models, auth, views
