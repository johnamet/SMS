#!/usr/bin/python3
"""
Service v1 app.
"""
import base64
import os
from os import environ

from dotenv import find_dotenv, load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher
from cryptography.hazmat.primitives.ciphers.modes import GCM
from apscheduler.schedulers.background import BackgroundScheduler

from models import storage
from modules.service.v1.microservices import services

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = environ.get('APP_SECRET')
app.register_blueprint(services)
CORS(app, resources={r"/services/v1/*": {"origins": "*"}})
jwt = JWTManager(app)


# Function to rotate secret key
def rotate_secret_key():
    # Implement logic to generate a new secret key
    new_secret_key = generate_app_secret()
    app.config['JWT_SECRET_KEY'] = new_secret_key


# Schedule token rotation
scheduler = BackgroundScheduler()
scheduler.add_job(rotate_secret_key, 'interval', hours=2)  # Rotate key every 24 hours
scheduler.start()


def generate_app_secret(length=32):
    """
  Generates a cryptographically secure app secret of specified length.

  Args:
      length (int, optional): Length of the secret in bytes. Defaults to 32 (256 bits).

  Returns:
      str: The generated app secret (base64 encoded).
  """
    # Generate random key and initialization vector (IV)
    key = os.urandom(32)  # 256-bit key
    iv = os.urandom(12)  # 96-bit IV

    # Create cipher object
    cipher = Cipher(algorithms.AES(key), GCM(iv), default_backend())
    encryptor = cipher.encryptor()

    # Hash a random string to create secret data
    hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hasher.update(os.urandom(100))  # Generate random data for hashing
    secret_data = hasher.finalize()

    # Encrypt the secret data
    ciphertext = encryptor.update(secret_data) + encryptor.finalize()

    # Encode the ciphertext for storage/transmission
    return base64.b64encode(iv + ciphertext).decode('utf-8')


@app.before_request
def before_request():
    # prompt user to log in to get an access token
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
