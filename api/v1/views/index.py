#!/usr/bin/python3
"""Index route"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def views():
    """Returns status in json format"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count():
    storage.count()