from collections import OrderedDict
from app import db


class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    department = db.Column(db.String(32))
    errors = db.relationship('Error', backref='contact', lazy=True)

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
    serial_number = db.Column(db.String(32))
    ip_address = db.Column(db.String(32))
    errors = db.relationship('Error', backref='instrument', lazy=True)

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
    description = db.Column(db.String(256))
    is_resolved = db.Column(db.Boolean)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
        nullable=False)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'),
        nullable=False)

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
                'is_resolved': self.is_resolved,
                'contact': self.contact.format(),
                'instrument': self.instrument.format(),
            }
        )