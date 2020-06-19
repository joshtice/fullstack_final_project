import os

# Auth0 configs
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', '')
ALGORITHMS = os.environ.get('ALGORITHMS', '').split()
API_AUDIENCE = os.environ.get('API_AUDIENCE', '')
CLIENT_ID = os.environ.get('CLIENT_ID', '')

# Miscellaneous configs
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEBUG = False
RECORDS_PER_PAGE = 20
SQLALCHEMY_TRACK_MODIFICATIONS = False
