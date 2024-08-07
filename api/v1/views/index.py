#!/usr/bin/python3
"""Index route"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
    }


@app_views.route('/status', methods=['GET'])
def views():
    """Returns status in json format"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    dict = {}
    for cls in classes:
        dict[cls] = storage.count(classes[cls])
    return jsonify(dict)
