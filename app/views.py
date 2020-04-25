from app import app
from .models import Contact, Instrument, Error
from flask import jsonify, abort, request


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'status': 'healthy',
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
    try:
        contact = Contact.query.get(id)
        return jsonify(contact.format()), 200
    except:
        abort(404)

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
    try:
        instrument = Instrument.query.get(id)
        return jsonify(instrument.format()), 200
    except:
        abort(404)

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
    try:
        error = Error.query.get(id)
        return jsonify(error.format()), 200
    except:
        abort(404)





@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            'error_code': 404,
            'error_message': 'The record or resource was not found.'
        }
    ), 404