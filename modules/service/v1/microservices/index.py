#!/usr/bin/python3
from flask import jsonify, make_response

from modules.service.v1.microservices import services


@services.route('/', methods=['GET'])
def get_status():
    return make_response(jsonify({"status": "ok"}), 200)