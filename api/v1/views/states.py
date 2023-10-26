#!/usr/bin/python3
"""This module creates a new view for State objects"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """This function retrieves a list of all State objects"""
    states = storage.all(State)
    state_list = []
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)

# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """This function retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

# Deletes a State object: DELETE /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """This function deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

# Creates a State: POST /api/v1/states
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """This function creates a State"""
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in state_json:
        abort(400, 'Missing name')
    state = State(**state_json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

# Updates a State object: PUT /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """This function updates a State object"""
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
