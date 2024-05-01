#!/usr/bin/python3
"""
Service v1 app.
"""
from os import environ

from dotenv import find_dotenv, load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from models import storage
# from flasgger import Swagger
from modules.service.v1.microservices import services
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = environ.get('APP_SECRET')
app.register_blueprint(services)
CORS(app, resources={r"/modules/service/v1/*": {"origins": "*"}})
jwt = JWTManager(app)


@app.before_request
def before_request():
    # prompt user to log in to get an access token
    print("Before request", request.endpoint)
    if request.endpoint not in ['services.login']:
        verify_jwt_in_request()


@app.teardown_appcontext
def close_db(exception):
    """Closes the database again at the end of the request."""
    storage.close()


@app.errorhandler(400)
def bad_request(error):
    """
    Error handler for 400 Bad Request.

    Args:
        error: The error message.

    Returns:
        JSON: Error message.
    """
    return make_response(jsonify({"error": str(error)}), 400)


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for 404 Not Found.

    Args:
        error: The error message.

    Returns:
        JSON: Error message.
    """
    return make_response(jsonify({"error": str(error)}), 404)


@app.errorhandler(500)
def internal_server_error(error):
    """
    Error handler for 500 Internal Server Error.

    Args:
        error: The error message.

    Returns:
        JSON: Error message.
    """
    return make_response(jsonify({"error": str(error)}), 500)


app.config["SWAGGER"] = {
    "swagger": "2.0",
    "title": "Service v1 API",
    "version": "1.0.0",
}

Swagger(app)

if __name__ == "__main__":
    host = environ.get("HOST", "0.0.0.0")
    port = int(environ.get("PORT", 8080))
    debug = environ.get("DEBUG", True)
    app.run(host=host, port=port, debug=debug, threaded=True)
