import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__, instance_relative_config=True)

    # Load default configuration
    app.config.from_object('config.default')

    # Determine whether running development or production, and load 
    # environment variables appropriately
    config_dict = {
        'development': 'config.development',
        'test': 'config.test',
        'production': 'config.production',
    }
    app.config.from_object(config_dict[os.environ.get('APP_MODE')])

    db.init_app(app)
    migrate.init_app(app)

    return app

app = create_app()
from app import models, auth, views
