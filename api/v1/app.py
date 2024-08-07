#!/usr/bin/python3
"""The Abnb API"""

from os import getenv
from models import storage
from flask import Flask

app = Flask(__name__)

from api.v1.views import app_views

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', "0.0.0.0"),
        port=int(getenv('HBNB_API_PORT', 5000)),
        threaded=True
    )
