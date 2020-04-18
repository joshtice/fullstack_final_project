from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('config.default')
# Load instance variables, including secrets
app.config.from_pyfile('config.py')
# Load configurations specified by environment variable
app.config.from_envvar('APP_CONFIG_FILE')

from app import views
