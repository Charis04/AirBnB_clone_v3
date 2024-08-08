#!/usr/bin/python3
"""A view for City objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import abort, request
from models.city import City
from models.state import State
from models import storage
import json


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
    )
def get_cities(state_id):
    """Retrieves the list of all cities of a State"""
    # Check if state with state_id exists
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # Get list of cities associated with state
    cities = [city.to_dict() for city in state.cities]
    return json.dumps(cities, indent=4)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city"""
    cities = [city.to_dict() for city in storage.all(City).values()]
    for city in cities:
        if city['id'] == city_id:
            return json.dumps(city, indent=4)
    abort(404)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False
    )
def create_city(state_id):
    """Creates a city"""
    # Get list of state ids and check if state_id is linked to any state
    state_id_list = [
        state.to_dict()['id'] for state in storage.all(State).values()
    ]
    if state_id not in state_id_list:
        abort(404)

    # Check if request contains valid json
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        return "Missing name", 400
    try:
        data = request.get_json()
        data["state_id"] = state_id
        city = City(**data)
    except ValueError:
        abort(400, "Not a JSON")
    storage.new(city)
    storage.save()
    return json.dumps(city.to_dict(), indent=4), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city"""
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    for attr, value in data.items():
        setattr(city, attr, value)
    city.save()
    return json.dumps(city.to_dict(), indent=4), 200


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_city(city_id):
    """Deletes a city"""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return {}, 200
    abort(404)
