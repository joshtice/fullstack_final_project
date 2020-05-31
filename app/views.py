from app import app
from .models import Contact, Instrument, Error
from .auth import AuthError, requires_auth
from flask import abort, jsonify, redirect, request
from datetime import datetime


def generate_login_uri():
    """
    Contruct the appropriate endpoint URI to direct the user to a login
    page
    """

    login_uri = (
        f"https://{app.config['AUTH0_DOMAIN']}/authorize"
        f"?audience={app.config['API_AUDIENCE']}"
        f"&response_type=token"
        f"&client_id={app.config['CLIENT_ID']}"
        f"&redirect_uri={app.config['REDIRECT_URI']}"
    )

    return login_uri


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'status': 'healthy',
        }
    ), 200

@app.route('/login', methods=['GET'])
def login():
    return redirect(generate_login_uri())

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
@requires_auth('read:contacts')
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.format()), 200

@app.route('/contacts/<int:id>/errors', methods=['GET'])
@requires_auth('read:contacts')
@requires_auth('read:errors')
def get_contact_errors(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(
        {
            'errors': [error.format() for error in contact.errors],
        }
    ), 200

@app.route('/contacts', methods=['POST'])
@requires_auth('create:contacts')
def post_contact():
    try:
        contact = Contact(**request.get_json())
        contact.insert()
        return jsonify(contact.format()), 200
    except:
        abort(400)

@app.route('/contacts/<int:id>', methods=['PATCH'])
@requires_auth('update:contacts')
def patch_contact(id):
    try:
        contact = Contact.query.get_or_404(id)
        for key in request.get_json():
            setattr(contact, key, request.get_json()[key])
        contact.update()
        return jsonify(contact.format()), 200
    except Error as e:
        abort(400)

@app.route('/contacts/<int:id>', methods=['DELETE'])
@requires_auth('delete:contacts')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    contact.delete()
    return jsonify(contact.format()), 200


########################################################################
# Instruments
########################################################################

@app.route('/instruments', methods=['GET'])
@requires_auth('read:instruments')
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
@requires_auth('read:instruments')
def get_instrument(id):
    instrument = Instrument.query.get_or_404(id)
    return jsonify(instrument.format()), 200

@app.route('/instruments/<int:id>/errors', methods=['GET'])
@requires_auth('read:instruments')
@requires_auth('read:errors')
def get_instrument_errors(id):
    instrument = Instrument.query.get_or_404(id)
    return jsonify({
        'errors': [error.format() for error in instrument.errors],
    }), 200

@app.route('/instruments', methods=['POST'])
@requires_auth('create:instruments')
def post_instrument():
    try:
        instrument = Instrument(**request.get_json())
        instrument.insert()
        return jsonify(instrument.format()), 200
    except:
        abort(400)

@app.route('/instruments/<int:id>', methods=['PATCH'])
@requires_auth('update:instruments')
def patch_instrument(id):
    try:
        instrument = Instrument.query.get_or_404(id)
        for key in request.get_json():
            setattr(instrument, key, request.get_json()[key])
        instrument.update()
        return jsonify(instrument.format()), 200
    except:
        abort(400)

@app.route('/instruments/<int:id>', methods=['DELETE'])
@requires_auth('delete:instruments')
def delete_instrument(id):
    instrument = Instrument.query.get_or_404(id)
    instrument.delete()
    return jsonify(instrument.format()), 200


########################################################################
# Errors
########################################################################

@app.route('/errors', methods=['GET'])
@requires_auth('read:errors')
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
@requires_auth('read:errors')
def get_error(id):
    error = Error.query.get_or_404(id)
    return jsonify(error.format()), 200

@app.route('/errors', methods=['POST'])
@requires_auth('create:errors')
def post_error():
    try:
        data = request.get_json()
        contact = Contact.query.get_or_404(data['contact'])
        instrument = Instrument.query.get_or_404(data['instrument'])
        date = (
            datetime.strptime(data['date'], app.config['DATE_FORMAT']) 
            if 'date' in data 
            else datetime.utcnow()
        )
        error = Error(
            description=data['description'],
            contact=contact,
            instrument=instrument,
            date=date,
            is_resolved=data.get('is_resolved', False)
        )
        error.insert()
        return jsonify(error.format()), 200
    except:
        abort(400)

@app.route('/errors/<int:id>', methods=['PATCH'])
@requires_auth('update:errors')
def patch_error(id):
    try:
        error = Error.query.get_or_404(id)
        data = request.get_json()
        if 'contact' in data:
            error.contact = Contact.query.get_or_404(data['contact'])
        if 'instrument' in data:
            error.instrument = Instrument.query.get_or_404(data['instrument'])
        if 'description' in data:
            error.description = data['description']
        if 'date' in data:
            error.date = datetime.strptime(data['date'], app.config['DATE_FORMAT'])
        if 'is_resolved' in data:
            error.is_resolved = data['is_resolved']
        error.update()
        return jsonify(error.format()), 200
    except:
        abort(400)

@app.route('/errors/<int:id>', methods=['DELETE'])
@requires_auth('delete:errors')
def delete_error(id):
    error = Error.query.get_or_404(id)
    deleted_record = error.format()
    error.delete()
    return jsonify(deleted_record), 200


########################################################################
# Error Handlers
########################################################################

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify(
        {
            'status_code': 400,
            'message': 'The request was not formed correctly',
        }
    ), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            'status_code': 404,
            'message': 'The record or resource was not found',
        }
    ), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify(
        {
            'status_code': 500,
            'message': 'A server error occurred',
        }
    ), 500

@app.errorhandler(AuthError)
def authorization_error(error):
    return jsonify(
        {
            'status_code': error.error_code,
            'message': error.error_message,
        }
    ), error.error_code