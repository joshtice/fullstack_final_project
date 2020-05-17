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


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            contact1 = Contact('contact', '1', 'department1')
            contact2 = Contact('contact', '2', 'department2')
            instrument1 = Instrument('SN001', '0.0.0.1')
            instrument2 = Instrument('SN002', '0.0.0.2')
            error1 = Error('broken', contact1, instrument1)
            contact1.insert()
            contact2.insert()
            instrument1.insert()
            instrument2.insert()
            error1.insert()
        yield client

@pytest.fixture(scope='module')
def admin_auth():
    yield {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.environ.get('ADMIN_TOKEN')}"
    }


def test_database_setup():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == (
        'postgres://app_test_user@localhost:5432/error_logging_app_test')

def test_client_status(client):
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'healthy'}

def test_contacts_get(client, admin_auth):
    response=client.get('/contacts', headers=admin_auth)
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data['contacts'] == [
        {
            'id': 1,
            'first_name': 'contact',
            'last_name': '1',
            'department': 'department1',
        },
        {
            'id': 2,
            'first_name': 'contact',
            'last_name': '2',
            'department': 'department2',
        },
    ]

def test_contacts_post(client, admin_auth):
    data = {
        'first_name': 'contact',
        'last_name': '3',
        'department': 'department3',
    }
    response = client.post(
        '/contacts', data=json.dumps(data), headers=admin_auth)
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data == {
        'id': 3,
        'first_name': 'contact',
        'last_name': '3',
        'department': 'department3',
    }

def test_contacts_patch(client, admin_auth):
    data = {
        'first_name': 'contact',
        'last_name': '3',
        'department': 'new department value',
    }
    response = client.patch(
        '/contacts/3', data=json.dumps(data), headers=admin_auth)
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data == {
        'id': 3,
        'first_name': 'contact',
        'last_name': '3',
        'department': 'new department value',
    }

def test_contacts_delete(client, admin_auth):
    response = client.delete('/contacts/3', headers=admin_auth)
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data == {
        'id': 3,
        'first_name': 'contact',
        'last_name': '3',
        'department': 'department3',
    }

def test_instruments_get(client, admin_auth):
    response=client.get('/instruments', headers=admin_auth)
    assert response.status_code == 200

def test_contacts_delete(client):
    assert 1 == 1

