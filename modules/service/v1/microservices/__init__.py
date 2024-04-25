#!/usr/bin/python3
"""Blueprint for microservices."""
from flask import Blueprint

services = Blueprint('services', __name__, url_prefix='/services/v1')

import modules.service.v1.microservices.attendace_service
from modules.service.v1.microservices.index import *
from modules.service.v1.microservices.attendace_service import *
from modules.service.v1.microservices.course_service import *
from modules.service.v1.microservices.class_service import *