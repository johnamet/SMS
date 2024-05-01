#!/usr/bin/python3
"""
The authentication service module
"""
from datetime import datetime, timedelta
from os import environ as env

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

with open('private.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), None, default_backend())

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = env.get("APP_SECRET")
jwt = JWTManager(app)

blacklist = set()


@jwt.invalid_token_loader
def invalid_token():
    return jsonify({'message': 'Token is invalid'}), 401


@app.route('/auth', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()

    print(data)
    try:
        if not data:
            return jsonify({'message': 'No data'}), 400

        email = data['email']
        password = data['password']
        id_ = data["id"]

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        additional_claims = {'email': email,
                             'password': password,
                             'client_id': env.get("CLIENT_ID"),
                             'client_secret': env.get("CLIENT_SECRET"),
                             'iss': 'http://localhost:8000/auth',
                             'exp': datetime.utcnow() + timedelta(minutes=30)}

        token = create_access_token(identity=id_, additional_claims=additional_claims)

        # token = jwt.encode(additional_claims, private_key, algorithm='RS256')

        access_token = token
    except Exception as e:
        return jsonify({'message': str(e)}), 500

    return jsonify({"access_token": access_token}), 200


@app.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    try:
        # Get the raw JWT token from the request
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'No token provided'}), 401

        # Add token to blacklist
        blacklist.add(token)

        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500


# Check if token is revoked
# @jwt.token_in_blocklist_loader()
# def check_token_in_blacklist(decrypted_token):
#     return decrypted_token['jti'] in blacklist


if __name__ == '__main__':
    app.run(host=env.get("AUTH_SERVER_HOST", "0.0.0.0"), port=env.get("AUTH_SERVER_PORT", 8080))
