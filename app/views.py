from app import app
from flask import jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'test_key': 'test_value',
        }
    )

@app.route('/user/<int:id>', methods=['GET'])
def user(id):
    user = User.query.filter_by(id=id)
    return jsonify(user.format())