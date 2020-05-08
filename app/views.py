from app import app
from .models import Contact, Instrument, Error
from .auth import AuthError, requires_auth
from flask import abort, jsonify, redirect, request


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'status': 'healthy',
        }
    ), 200

@app.route('/login', methods=['GET'])
def login():
    return redirect("https://dev-udacity.auth0.com/")

########################################################################
# Contacts
########################################################################

@app.route('/contacts', methods=['GET'])
@requires_auth('read:contacts')
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
            contact[key] = request.get_json()[key]
        contact.update()
        return jsonify(contact.format()), 200
    except:
        abort(400)

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    contact.delete()
    return jsonify(contact.format()), 200


########################################################################
# Instruments
########################################################################

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
    instrument = Instrument.query.get_or_404(id)
    return jsonify(instrument.format()), 200

@app.route('/instruments/<int:id>/errors', methods=['GET'])
def get_instrument_errors(id):
    instrument = Instrument.query.get_or_404(id)
    return jsonify({
        'errors': [error.format() for error in instrument.errors],
    }), 200

@app.route('/instruments', methods=['POST'])
def post_instrument():
    instrument = Instrument(**request.get_json())
    try:
        instrument.insert()
        return jsonify(instrument.format()), 200
    except:
        abort(400)

@app.route('/instruments/<int:id>', methods=['PATCH'])
def patch_instrument(id):
    instrument = Instrument.query.get_or_404(id)
    try:
        for key in request.get_json():
            instrument[key] = request.get_json()[key]
        instrument.update()
        return jsonify(instrument.format()), 200
    except:
        abort(400)

@app.route('/instruments/<int:id>', methods=['DELETE'])
def delete_instrument(id):
    instrument = Instrument.query.get_or_404(id)
    instrument.delete()
    return jsonify(instrument.format()), 200


########################################################################
# Errors
########################################################################

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
    error = Error.query.get_or_404(id)
    return jsonify(error.format()), 200

@app.route('/errors', methods=['POST'])
def post_error():
    error = Error(**request.get_json())
    try:
        error.insert()
        return jsonify(error.format()), 200
    except:
        abort(400)

@app.route('/errors/<int:id>', methods=['PATCH'])
def patch_error(id):
    error = Error.query.get_or_404(id)
    try:
        for key in request.get_json():
            error[key] = request.get_json()[key]
        error.update()
        return jsonify(error.format()), 200
    except:
        abort(400)

@app.route('/errors/<int:id>', methods=['DELETE'])
def delete_error(id):
    error = Error.query.get_or_404(id)
    error.delete()
    return jsonify(error.format()), 200


########################################################################
# Error Handlers
########################################################################

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

@app.errorhandler(AuthError)
def authorization_error(error):
    return jsonify(
        {
            'error_code': error.error_code,
            'error_message': error.error_message,
        }
    ), error.error_code