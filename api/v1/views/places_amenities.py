#!/usr/bin/python3
"""
Create a view for the link between Place objects and Amenity objects
and that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
