from datetime import datetime
from app import db


class Contact(db.Model):

    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    department = db.Column(db.String(32))
    errors = db.relationship('Error', backref='contact', lazy=True)

    def __init__(self, first_name, last_name, department):
        self.first_name = first_name
        self.last_name = last_name
        self.department = department

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return ( 
            {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'department': self.department,
            }
        )


class Instrument(db.Model):

    __tablename__ = 'instrument'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(32), nullable=False)
    ip_address = db.Column(db.String(32))
    errors = db.relationship(
        'Error', backref='instrument', lazy=True, cascade='all, delete'
    )

    def __init__(self, serial_number, ip_address):
        self.serial_number = serial_number
        self.ip_address = ip_address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return (
            {
                'id': self.id,
                'serial_number': self.serial_number,
                'ip_address': self.ip_address,
            }
        )


class Error(db.Model):

    __tablename__ = 'error'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(256), nullable=False)
    is_resolved = db.Column(db.Boolean, nullable=False, default=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
        nullable=False)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'),
        nullable=False)

    def __init__(self, description, contact, instrument, date=datetime.utcnow(), 
        is_resolved=False):
        self.description = description
        self.contact = contact
        self.instrument = instrument
        self.date = date
        self.is_resolved = is_resolved

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return (
            {
                'id': self.id,
                'description': self.description,
                'date': self.date,
                'is_resolved': self.is_resolved,
                'contact': self.contact.format(),
                'instrument': self.instrument.format(),
            }
        )