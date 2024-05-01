#!/usr/bin/python3
"""
The authentication service module
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from flask_jwt_extended import jwt_required, JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask import Flask, jsonify, request
from dotenv import find_dotenv, load_dotenv
from os import environ as env
import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

with open('private.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), None, default_backend())

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = env.get("APP_SECRET")
jwt = JWTManager(app)


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
                             'iss': 'http://localhost:8000/auth'}

        token = create_access_token(identity=id_, additional_claims=additional_claims)

        # token = jwt.encode(additional_claims, private_key, algorithm='RS256')

        access_token = token
    except Exception as e:
        return jsonify({'message': str(e)}), 500

    return jsonify({"access_token": access_token}), 200


@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
