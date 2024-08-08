#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all states"""
    states = storage.all(State)
    states_list = []
    for obj in states:
        states_list.append(states[obj].to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_state(state_id):
    """Deletes a state"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return {}, 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state"""
    if not request.json:
        return "Not a JSON", 400
    if 'name' not in request.json:
        return "Missing name", 400
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state"""
    if not request.json:
        return "Not a JSON", 400
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    for attr, value in data.items():
        setattr(state, attr, value)
    state.save()
    return jsonify(state.to_dict()), 200
