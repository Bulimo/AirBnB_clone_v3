#!/usr/bin/python3
"""This module creates a new view for State objects"""

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """This function retrieves a list of all State objects"""
    states = storage.all(State)
    state_list = []
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)
