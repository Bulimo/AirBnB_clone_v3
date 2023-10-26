#!/usr/bin/python3
""" index.py - index file for api/v1/views folder """

from api.v1.views import app_views
from flask import jsonify


# create  a route /status on the object app_views that returns a JSON
# status response
@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns a JSON status response """
    # return {"status": "OK"}
    # jsonify function converts a python dict to JSON string
    return jsonify({"status": "OK"})
