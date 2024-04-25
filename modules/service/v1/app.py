#!/usr/bin/python3
"""
Service v1 app.
"""
from flask_cors import CORS
from flask import Blueprint
from os import environ
from flask import Flask, jsonify, make_response
# from flasgger import Swagger
from modules.service.v1.microservices import services
from models import storage

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(services)
CORS(app, resources={r"/modules/service/v1/*": {"origins": "*"}})


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
    return make_response(jsonify({"error": "Internal Server Error", "error_msg": {error}}), 500)


app.config["SWAGGER"] = {
    "swagger": "2.0",
    "title": "Service v1 API",
    "version": "1.0.0",
}

# Swagger(app)

if __name__ == "__main__":
    host = environ.get("HOST", "0.0.0.0")
    port = int(environ.get("PORT", 8080))
    debug = environ.get("DEBUG", True)
    app.run(host=host, port=port, debug=debug, threaded=True)
