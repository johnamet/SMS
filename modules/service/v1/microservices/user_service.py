#!/usr/bin/python3
"""
The management service
"""
from datetime import datetime, timedelta, UTC

import requests
from flasgger import swag_from
from flask import jsonify, request, abort, make_response

from modules.service.v1.microservices import services
from modules.user_management.user_management import UserManagement

user_management = UserManagement()


@services.route('/login', methods=['POST'], strict_slashes=False)
@swag_from('swagger_docs/login.yml')
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role', None)

    if not email or not password:
        abort(400, 'Email and password are required')

    # if not role:
    #     abort(400, 'Role is required. eg. parent, teacher, admin, etc')

    try:
        user, msg = user_management.login(email, password, role)

        if not user:
            abort(404, 'Access denied')

    except ValueError as e:
        abort(400, str(e))

    except Exception as e:
        abort(500, str(e))

    data["id"] = user.id

    r = requests.post('http://127.0.0.1:8004/auth', json=data)

    if r.status_code == 200:
        response = {
            'access_token': r.json()['access_token'],
            'user_id': user.id,
            'token_type': 'jwt',
            'expires_in': datetime.now() + timedelta(minutes=30),
        }

        user_management.update_user(user.id, **{"last_login_date": datetime.now(UTC),
                                                "last_login_ip": request.remote_addr})

    else:
        return jsonify({"message": "Failed to create access token. Please try again.", "error": r.text}), r.status_code
    return jsonify(response), 200


@services.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    data = request.headers

    authorization = data.get('Authorization')

    if not authorization:
        abort(400, 'Missing Authorization')

    r = requests.post('http://127.0.0.1:8000/auth', json=jsonify({"access_token": authorization}))

    return jsonify(r.json()), r.status_code


@services.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Get all users

    Returns:
        JSON: List of users
    """
    try:
        users, msg = user_management.get_all_users()
        if users:
            users_dict = {user.id: user.serialize() for user in users}
            results = {
                'users': users_dict,
                'message': msg
            }

            return make_response(jsonify(results), 200)
        else:
            return make_response(jsonify({"message": "No users found."}), 404)

    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Get a user

    Args:
        user_id (str): User ID

    Returns:
        JSON: User details
    """
    try:
        user, msg = user_management.get_user(user_id)
        result = {user.id: user.serialize(), "status_msg": msg}
        return make_response(jsonify(result), 200)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/staff", methods=['GET'], strict_slashes=False)
def get_all_staff():
    """
    Get all staff users

    Returns:
        JSON: List of staff
    """

    try:
        staffs, msg = user_management.get_all_staff()
        staffs = [user_management.get_staff_details(staff.id)[0] for staff in staffs]
        staff_dict = {staff["id"]: staff for staff in staffs}
    except ValueError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")

    return make_response(jsonify({"staff": staff_dict, "status_msg": msg}), 200)


@services.route("/users/staff/<staff_id>", methods=['GET'], strict_slashes=False)
def get_staff_user(staff_id):
    """
    Get the detail information of a staff

    Args:
        staff_id (str): Staff ID

    Returns:
        JSON: Staff details
    """

    try:
        staff, msg = user_management.get_staff_details(staff_id)
        staff_dict = {staff["id"]: staff}
        result = {"status_msg": msg}
        result.update(staff_dict)
        return make_response(jsonify(result), 200)
    except ValueError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/parents/", methods=['GET'], strict_slashes=False)
def get_all_parents():
    """
    Get all parent users

    Returns:
        JSON: List of parent users
    """

    try:
        parents, msg = user_management.get_all_parent()
        parents = [user_management.get_parent_details(parent.id)[0] for parent in parents]
        parents_dict = {parent["id"]: parent for parent in parents}
    except ValueError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")

    return make_response(jsonify({"parents": parents_dict, "status_msg": msg}), 200)


@services.route("/users/parents/<parent_id>", methods=['GET'], strict_slashes=False)
def get_parent_user(parent_id):
    try:
        parent, msg = user_management.get_parent_details(parent_id)
        parent_dict = {parent["id"]: parent}
        result = {"status_msg": msg}
        result.update(parent_dict)
        return make_response(jsonify(result), 200)
    except ValueError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new user
    """
    response = request.get_json()

    if response is None:
        abort(400, "No data")

    if 'email' not in response:
        abort(400, "No email")

    if 'password' not in response:
        abort(400, "No password")

    if 'first_name' not in response:
        abort(400, "No first_name")
    if 'last_name' not in response:
        abort(400, "No last_name")

    if 'gender' not in response:
        abort(400, 'No gender')
    try:

        user, msg = user_management.create_user(response)
        result = {user.id: user.serialize(), "status_msg": msg}
        return make_response(jsonify(result), 200)
    except ValueError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    try:
        status, msg = user_management.delete_user(user_id)
        return jsonify({"status": status, "msg": msg}), 200
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/staff/<user_id>", methods=['POST'], strict_slashes=False)
def create_staff(user_id):
    """
    Create a staff user
    """
    try:
        response = request.get_json()
        if response is None:
            abort(400, "No data")

        if 'role' not in response:
            abort(400, "No role")

        if user_id is None:
            abort(400, "No user_id")

        staff, msg = user_management.create_staff(user_id, role=response['role'], **response)

        result = {staff.id: staff.serialize(), "status_msg": msg}
        return make_response(jsonify(result), 200)

    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/staff/<staff_id>", methods=['DELETE'], strict_slashes=False)
def delete_staff(staff_id):
    """
    Delete a staff user
    """

    try:
        status, msg = user_management.delete_staff(staff_id)
        return jsonify({"status": status, "msg": msg}), 200
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/parents/<user_id>", methods=['POST'], strict_slashes=False)
def create_user_parent(user_id):
    """
    create a new parent user
    """

    try:
        response = request.get_json()
        if response is None:
            return abort(400, "No data")

        status, msg = user_management.create_parent(user_id, **response)
        return jsonify({"status": status, "msg": msg}), 200
    except ValueError as e:
        return abort(404, str(e))
    except Exception as e:
        return abort(500, f"Internal Server Error: {str(e)}")


@services.route("/users/parents/<parent_id>", methods=['DELETE'], strict_slashes=False)
def delete_parent(parent_id):
    try:
        status, msg = user_management.delete_parent(parent_id)
        return jsonify({"status": status, "msg": msg}), 200
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")
