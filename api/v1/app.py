#!/usr/bin/python3
""" Module for app.py """
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


# create a variable app, instance of Flask
app = Flask(__name__)

# set strict_slashes to False for all routes
app.url_map.strict_slashes = False

# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


# declare a method to handle @app.teardown_appcontext
@app.teardown_appcontext
def teardown_appcontext(self):
    """ Method to handle teardown or when application closes"""
    storage.close()


if __name__ == "__main__":
    """ run flask sever with defaults 5000 and 0.0.0.0 """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    # run the flask application
    # set threaded to be true so that it can serve multiple clients
    app.run(host=host, port=port, threaded=True)
