#!/usr/bin/python3
""" __init__ file for api/v1/views folder"""

from flask import Blueprint

# create a variable app_views which is an instance of Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
