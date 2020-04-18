from app import app
from flask import jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'test_key': 'test_value',
        }
    )
