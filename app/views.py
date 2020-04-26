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
    page = request.args.get('page', default=1, type=int)
    query = {
        key: request.args[key] for key in request.args if key != 'page'
    }
    if request.args:
        contacts = Contact.query.filter_by(**query).paginate(
            page=page, 
            per_page=app.config['RECORDS_PER_PAGE'], 
            error_out=False
        )
    else:
        contacts = Contact.query.paginate(
            page=page, per_page=app.config['RECORDS_PER_PAGE'], error_out=False
        )
    return jsonify(
        {
            'page': page,
            'contacts': [contact.format() for contact in contacts.items],
        }
    ), 200

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.format()), 200

@app.route('/contacts/<int:id>/errors', methods=['GET'])
def get_contact_errors(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(
        {
            'errors': [error.format() for error in contact.errors],
        }
    ), 200

@app.route('/contacts', methods=['POST'])
def post_contact():
    contact = Contact(**request.get_json())
    try:
        contact.insert()
        return jsonify(contact.format()), 200
    except:
        abort(400)

@app.route('/contacts/<int:id>', methods=['PATCH'])
def patch_contact(id):
    contact = Contact.query.get_or_404(id)
    try:
        for key in request.get_json():
            contact[key] = request.get_json()['key']
        contact.update()
        return jsonify(contact.format()), 200
    except:
        abort(400)

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    contact.delete()
    return jsonify(contact.format()), 200



@app.route('/instruments', methods=['GET'])
def get_all_instruments():
    page = request.args.get('page', default=1, type=int)
    query = {
        key: request.args[key] for key in request.args if key != 'page'
    }
    if request.args:
        instruments = Instrument.query.filter_by(**query).paginate(
            page=page, 
            per_page=app.config['RECORDS_PER_PAGE'], 
            error_out=False
        )
    else:
        instruments = Instrument.query.paginate(
            page=page, per_page=app.config['RECORDS_PER_PAGE'], error_out=False
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

@app.route('/instruments/<int:id>/errors', methods=['GET'])
def get_instrument_errors(id):
    try:
        instrument = Instrument.query.get(id)
        return jsonify({
            'errors': [error.format() for error in instrument.errors],
        }), 200
    except:
        abort(404)



@app.route('/errors', methods=['GET'])
def get_all_errors():
    page = request.args.get('page', default=1, type=int)
    query = {
        key: request.args[key] for key in request.args if key != 'page'
    }
    if request.args:
        errors = Error.query.filter_by(**query).paginate(
            page=page, 
            per_page=app.config['RECORDS_PER_PAGE'], 
            error_out=False
        )
    else:
        errors = Error.query.paginate(
            page=page, per_page=app.config['RECORDS_PER_PAGE'], error_out=False
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



@app.errorhandler(400)
def bad_request_error(error):
    return jsonify(
        {
            'error_code': 400,
            'error_message': 'The request was not formed correctly.',
        }
    ), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            'error_code': 404,
            'error_message': 'The record or resource was not found.',
        }
    ), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify(
        {
            'error_code': 500,
            'error_message': 'A server error occurred.',
        }
    ), 500