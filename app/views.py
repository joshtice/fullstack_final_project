from app import app
from .models import Contact, Instrument, Error
from flask import jsonify, abort, request


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'test_key': 'test_value',
        }
    ), 200

@app.route('/contacts', methods=['GET'])
def get_all_contacts():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return jsonify(
        {
            'page': page,
            'contacts': [contact.format() for contact in contacts.items],
        }
    ), 200

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.filter_by(id=id).first_or_404()
    return jsonify(contact.format()), 200

@app.route('/instruments', methods=['GET'])
def get_all_instruments():
    page = request.args.get('page', 1, type=int)
    instruments = Instrument.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return jsonify(
        {
            'page': page,
            'instruments': [
                instrument.format() for instrument in instruments.items
            ],
        }
    ), 200

@app.route('/instruments/<int:id>', methods=['GET'])
def get_instrument(id):
    instrument = Instrument.query.filter_by(id=id).first_or_404()
    return jsonify(instrument.format()), 200

@app.route('/errors', methods=['GET'])
def get_all_errors():
    page = request.args.get('page', 1, type=int)
    errors = Error.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return jsonify(
        {
            'page': page,
            'errors': [
                error.format() for error in errors.items
            ],
        }
    ), 200

@app.route('/errors/<int:id>', methods=['GET'])
def get_error(id):
    error = Error.query.filter_by(id=id).first_or_404()
    return jsonify(error.format()), 200





@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            'error_code': 404,
            'error_message': 'The record or resource was not found.'
        }
    ), 404