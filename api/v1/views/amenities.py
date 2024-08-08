#!/usr/bin/python3
"""A view for Amenity objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import abort, request
from models.amenity import Amenity
from models import storage
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves all amenities"""
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    amenities_dict = [amenity.to_dict() for amenity in amenities.values()]
    return json.dumps(amenities_dict, indent=4)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False
    )
def get_amenity(amenity_id):
    """Retrieves an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return json.dumps(amenity, indent=4)
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenityy"""
    # Check if request contains valid json
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        return "Missing name", 400
    try:
        data = request.get_json()
        amenity = Amenity(**data)
    except ValueError:
        abort(400, "Not a JSON")
    storage.new(amenity)
    storage.save()
    return json.dumps(amenity.to_dict(), indent=4), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False
    )
def update_amenity(amenity_id):
    """Updates an amenity"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    for attr, value in data.items():
        setattr(amenity, attr, value)
    amenity.save()
    return json.dumps(amenity.to_dict(), indent=4), 200


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_amenity(amenity_id):
    """Deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}, 200
    abort(404)
