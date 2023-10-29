#!/usr/bin/python3
"""This module creates a new view for user objects"""

from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from flask import jsonify, abort, request


# Retrieves the list of all Place objects: /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


# Retrieves a Place object: /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


# Deletes a Place object: /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


# Creates a Place: /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


# Updates a Place object: /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


# retrieves all Place objects depending of the JSON in the body of the request.
@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """retrieves all Place objects depending on search request"""
    search_request = request.get_json()
    if not search_request:
        abort(400, description="Not a JSON")

    # If the JSON body is empty or each list of all keys are empty:
    # return all Place objects
    if len(search_request) == 0 or (len(search_request.get('cities')) == 0 and
                                    len(search_request.get('states')) == 0 and
                                    len(search_request.get('amenities')) == 0):
        places = []
        for place in storage.all(Place):
            places.append(place.to_dict())
        return jsonify(places), 200

    search_results = []  # store the results of search
    states = search_request.get('states')  # state_ids in request JSON
    cities = search_request.get('cities')  # city_ids in request JSON
    amenities = search_request.get('amenities')  # amenity_ids of request JSON
    all_places = []  # all places generated from State and City
    all_cities = []  # all cities generated from State and City
    # results should include all Place objects for each State id listed
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                state_cities = []
                if storage_t == 'db':
                    state_cities = state.cities
                else:
                    state_cities = state.cities()
                for city in state_cities:
                    all_cities.append(city)

    # results should include all Place objects for each City id listed
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in all_cities:
                all_cities.append(city)

    # get all the places for the cities
    if all_cities:
        if storage_t == 'db':
            for city in all_cities:
                places = city.places
                for place in places:
                    all_places.append(place)
        else:
            city_ids = [city.id for city in all_cities]
            places = storage.all(Place)
            for place in places:
                if places.city_id in city_ids:
                    all_places.append(place)

    # limit search results to only Place objects having all Amenity ids listed
    if amenities:
        for place in all_places:
            place_amenities = []    # store amenities in a place
            add = True
            if storage_t == 'db':
                place_amenities = place.amenities
            else:
                place_amenities = place.amenities()
            for amenity_id in amenities:
                amenity = storage.get(Amenity, amenity_id)
                if not amenity:
                    continue
                if amenity not in place_amenities:
                    add = False
                    break
                else:
                    add = True
            if add:
                search_results.append(place.to_dict())
    else:
        for place in all_places:
            search_results.append(place.to_dict())

    return jsonify(search_results), 200
