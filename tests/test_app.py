from datetime import datetime
import json
import base64
import os
import subprocess
import unittest
from flask_sqlalchemy import SQLAlchemy
from jose import jwt

from app import app, db
from app.models import Contact, Instrument, Error

from pprint import pprint

def generate_contact_jwt():
    pass

def generate_admin_jwt():
    pass


class TestErrorLoggingApp(unittest.TestCase):
    """
    Test the authorization, CRUD operations, and error handlers for app
    """

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        contacts = [
            Contact('jane', 'doe', 'system integration'),
            Contact('john', 'doe', 'assay development'),
        ]
        instruments = [
            Instrument('VRGN001', '127.0.0.24'),
            Instrument('VRGN002', '127.0.0.25'),
        ]
        errors = [
            Error('software freeze', contacts[0], instruments[0]),
            Error('broken bay', contacts[1], instruments[1]),
        ]
        [contact.insert() for contact in contacts]
        [instrument.insert() for instrument in instruments]
        [error.insert() for error in errors]

    def tearDown(self):
        db.session.close()
        db.session.remove()
        db.drop_all()

    def test_client(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

    def test_get_contacts(self):
        response = self.app.get('/contacts')
        # self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    subprocess.run(['psql', '-f', f'{os.getcwd()}/tests/setup_test_db.sql'])
    unittest.main(exit=False)
    pprint(locals().keys())
    subprocess.run(['psql', '-f', f'{os.getcwd()}/tests/teardown_test_db.sql'])