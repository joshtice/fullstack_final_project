from app import app
from .models import Contact, Instrument, Error
from flask import jsonify, abort


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'test_key': 'test_value',
        }
    )

@app.route('/contacts/<int:id>', methods=['GET'])
def get_user(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact:
        return jsonify(contact.format())
    else:
        abort(404)

@app.route('/instruments/<int:id>', methods=['GET'])
def get_instrument(id):
    instrument = Instrument.query.filter_by(id=id).first()
    if instrument:
        return jsonify(instrument.format())
    else:
        abort(404)

@app.route('/errors/<int:id>', methods=['GET'])
def get_error(id):
    error = Error.query.filter_by(id=id).first()
    if error:
        return jsonify(error.format())
    else:
        abort(404)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            'error_code': 404,
            'error_message': 'The record or resource was not found.'
        }
    )