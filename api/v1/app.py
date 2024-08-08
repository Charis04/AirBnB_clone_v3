#!/usr/bin/python3
"""The Abnb API"""

from os import getenv
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(400)
def not_json(error):
    return jsonify({'error': 'Not a JSON'}), 400


@app.teardown_appcontext
def teardown(exc):
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', "0.0.0.0"),
        port=int(getenv('HBNB_API_PORT', 5000)),
        threaded=True
    )
