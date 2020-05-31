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
            error1 = Error('broken', contact1, instrument1, datetime(2020, 1, 1))
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

@pytest.fixture(scope='module')
def contact_auth():
    yield {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.environ.get('CONTACT_TOKEN')}"
    }

@pytest.fixture(scope='module')
def expired_auth():
    yield {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.environ.get('EXPIRED_TOKEN')}"
    }


def test_database_setup():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == (
        'postgresql://app_test_user@localhost:5432/error_logging_app_test')

def test_client_status(client):
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'healthy'}

def test_contacts_get_success(client, admin_auth):
    response = client.get('/contacts', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json()['contacts'] == [
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

def test_contacts_get_failure(client):
    response = client.get('/contacts')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_contacts_get_one_success(client, admin_auth):
    response=client.get('/contacts/1', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 1,
        'first_name': 'contact',
        'last_name': '1',
        'department': 'department1'
    }

def test_contacts_get_one_failure(client):
    response = client.get('/contacts/1')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_contacts_post_success(client, admin_auth):
    data = {
        'first_name': 'contact',
        'last_name': '3',
        'department': 'department3',
    }
    response = client.post(
        '/contacts', data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 3,
        'first_name': 'contact',
        'last_name': '3',
        'department': 'department3',
    }

def test_contacts_post_failure(client, contact_auth):
    data = {
        'first_name': 'contact',
        'last_name': '3',
        'department': 'department3',
    }
    response = client.post(
        '/contacts', data=json.dumps(data), headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_contacts_patch_success(client, admin_auth):
    data = {
        'first_name': 'contact',
        'last_name': '3',
        'department': 'new department value',
    }
    response = client.patch(
        '/contacts/3', data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 3,
        'first_name': 'contact',
        'last_name': '3',
        'department': 'new department value',
    }

def test_contacts_patch_failure(client, contact_auth):
    data = {
        'first_name': 'contact',
        'last_name': '3',
        'department': 'new department value',
    }
    response = client.patch(
        '/contacts/3', data=json.dumps(data), headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_contacts_delete_success(client, admin_auth):
    response = client.delete('/contacts/3', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 3,
        'first_name': 'contact',
        'last_name': '3',
        'department': 'new department value',
    }

def test_contacts_delete_failure(client, contact_auth):
    response = client.delete('/contacts/3', headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_instruments_get_success(client, admin_auth):
    response = client.get('/instruments', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json()['instruments'] == [
        {
            'id': 1,
            'serial_number': 'SN001',
            'ip_address': '0.0.0.1',
        },
        {
            'id': 2,
            'serial_number': 'SN002',
            'ip_address': '0.0.0.2',
        },
    ]

def test_instruments_get_failure(client):
    response = client.get('/instruments')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_instruments_get_one_success(client, admin_auth):
    response = client.get('instruments/1', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 1,
        'serial_number': 'SN001',
        'ip_address': '0.0.0.1',
    }

def test_instruments_get_one_failure(client):
    response = client.get('instruments/1')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_instruments_post_success(client, admin_auth):
    data = {
        'serial_number': 'SN003',
        'ip_address': '0.0.0.3',
    }
    response = client.post(
        '/instruments', data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 3,
        'serial_number': 'SN003',
        'ip_address': '0.0.0.3',
    }

def test_instruments_post_failure(client, contact_auth):
    data = {
        'serial_number': 'SN003',
        'ip_address': '0.0.0.3',
    }
    response = client.post(
        '/instruments', data=json.dumps(data), headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_instruments_patch_success(client, admin_auth):
    data = {
        'serial_number': 'SN003',
        'ip_address': '0.0.0.5',
    }
    response = client.patch(
        '/instruments/3', data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 3,
        'serial_number': 'SN003',
        'ip_address': '0.0.0.5',
    }

def test_instruments_patch_failure(client, contact_auth):
    data = {
        'serial_number': 'SN003',
        'ip_address': '0.0.0.5',
    }
    response = client.patch(
        '/instruments/3', data=json.dumps(data), headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_instruments_delete_success(client, admin_auth):
    response = client.delete('/instruments/3', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 3,
        'serial_number': 'SN003',
        'ip_address': '0.0.0.5',
    }

def test_instruments_delete_failure(client, contact_auth):
    response = client.delete('/instruments/3', headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_errors_get_success(client, admin_auth):
    response = client.get('/errors', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json()['errors'] == [
        {
            'id': 1,
            'description': 'broken',
            'contact': {
                'id': 1,
                'first_name': 'contact',
                'last_name': '1',
                'department': 'department1',
            },
            'instrument': {
                'id': 1,
                'serial_number': 'SN001',
                'ip_address': '0.0.0.1',
            },
            'date': 'Wed, 01 Jan 2020 00:00:00 GMT',
            'is_resolved': False,
        }
    ]

def test_errors_get_failure(client):
    response = client.get('/errors')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_errors_get_one_success(client, admin_auth):
    response = client.get('/errors/1', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 1,
        'description': 'broken',
        'contact': {
            'id': 1,
            'first_name': 'contact',
            'last_name': '1',
            'department': 'department1',
        },
        'instrument': {
            'id': 1,
            'serial_number': 'SN001',
            'ip_address': '0.0.0.1',
        },
        'date': 'Wed, 01 Jan 2020 00:00:00 GMT',
        'is_resolved': False,
    }

def test_errors_get_one_failure(client):
    response = client.get('/errors/1')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_errors_post_success(client, admin_auth):
    data = {
        'description': 'broken',
        'contact': 1,
        'instrument': 1,
        'date': '2020-05-30 12:00:00',
        'is_resolved': False,
    }
    response = client.post('/errors', 
        data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 2,
        'description': 'broken',
        'contact': {
            'id': 1,
            'first_name': 'contact',
            'last_name': '1',
            'department': 'department1',
        },
        'instrument': {
            'id': 1,
            'serial_number': 'SN001',
            'ip_address': '0.0.0.1',
        },
        'date': 'Sat, 30 May 2020 12:00:00 GMT',
        'is_resolved': False,
    }

def test_errors_post_failure_failure(client):
    data = {
        'description': 'broken',
        'contact': 1,
        'instrument': 1,
        'date': '2020-05-30 12:00:00',
        'is_resolved': False,
    }
    response = client.post('/errors', data=json.dumps(data))
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_errors_patch_success(client, admin_auth):
    data = {
        'description': 'really broken',
        'contact': 2,
        'instrument': 2,
        'date': '2020-05-31 12:00:00',
        'is_resolved': True,
    }
    response = client.patch('/errors/2', 
                            data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 2,
        'description': 'really broken',
        'contact': {
            'id': 2,
            'first_name': 'contact',
            'last_name': '2',
            'department': 'department2',
        },
        'instrument': {
            'id': 2,
            'serial_number': 'SN002',
            'ip_address': '0.0.0.2',
        },
        'date': 'Sun, 31 May 2020 12:00:00 GMT',
        'is_resolved': True,
    }

def test_errors_patch_failure(client, contact_auth):
    data = {
        'description': 'really broken',
        'contact': 2,
        'instrument': 2,
        'date': '2020-05-31 12:00:00',
        'is_resolved': True,
    }
    response = client.patch('/errors/2', 
                            data=json.dumps(data), headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_errors_delete_success(client, admin_auth):
    response = client.delete('/errors/2', headers=admin_auth)
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 2,
        'description': 'really broken',
        'contact': {
            'id': 2,
            'first_name': 'contact',
            'last_name': '2',
            'department': 'department2',
        },
        'instrument': {
            'id': 2,
            'serial_number': 'SN002',
            'ip_address': '0.0.0.2',
        },
        'date': 'Sun, 31 May 2020 12:00:00 GMT',
        'is_resolved': True,
    }

def test_errors_delete_failure(client, contact_auth):
    response = client.delete('/errors/2', headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_400_malformed_request(client, admin_auth):
    data = {'incorrect key': 'incorrect value'}
    response = client.post('/contacts', data=json.dumps(data), headers=admin_auth)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'The request was not formed correctly'

def test_401_no_header(client):
    response = client.get('/errors')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authorization header missing'

def test_401_token_expired(client, expired_auth):
    response = client.get('errors', headers=expired_auth)
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Token expired'

def test_403_incorrect_permissions(client, contact_auth):
    response = client.post('/contacts', headers=contact_auth)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Correct permission not found - Access forbidden'

def test_404_resource_does_not_exist(client, admin_auth):
    response = client.get('/errors/1000', headers=admin_auth)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'The record or resource was not found'
