from datetime import datetime
import json
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jose import jwt
import subprocess

from app import create_app
from app.models import Contact, Instrument, Error

from pprint import pprint

import pytest


from app import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def admin_auth():
    yield {'Authorization': f"Bearer {os.environ.get('ADMIN_TOKEN')}"}


def test_database_setup():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == (
        'postgres://app_test_user@localhost:5432/error_logging_app_test')

def test_client_status(client):
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'healthy'}

@pytest.mark.skip()
def test_contacts_post(client, admin_auth_header):
    data = json.dumps({
        'first_name': 'contact',
        'last_name': '1',
        'department': 'department 1',
    })
    response = client.post(
        '/contacts', data=data, headers=admin_auth_header)
    assert response.status_code == 200
    # assert json.loads(response.data) == data

def test_contacts_get(client, admin_auth):
    response=client.get('/contacts', headers=admin_auth)
    assert response.status_code == 200

def test_instruments_get(client, admin_auth):
    response=client.get('/instruments', headers=admin_auth)
    assert response.status_code == 200

def test_contacts_delete(client):
    pass
